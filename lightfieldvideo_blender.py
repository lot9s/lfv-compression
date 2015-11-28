bl_info = {
    "name": "Add a lot of cameras",
    "category": "Object",
}

import bpy
from mathutils import *


class LightfieldVideo(bpy.types.Operator):
    """AddCamers"""      # blender will use this as a tooltip for menu items and buttons.
    bl_idname = "object.addcameras"        # unique identifier for buttons and menu items to reference.
    bl_label = "Add Some Cameras"         # display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # enable undo for the operator.
    horizontal = bpy.props.IntProperty(name="Horizontal dimension", default=5, min=1, max=100)
    vertical = bpy.props.IntProperty(name="Vertical dimension", default=5, min=1, max=100)
    horizontal_step = bpy.props.FloatVectorProperty(name="Horizontal step", default=(0, 0.1, 0))
    vertical_step = bpy.props.FloatVectorProperty(name="Vertical step", default=(0.1, 0, 0))
    center = bpy.props.FloatVectorProperty(name="Center of the grid", default=(0.0,0.,0.))
    direction = bpy.props.FloatVectorProperty(name="Rotation of the grid", default=(0.,0.,0.))
    base_path = bpy.props.StringProperty(name="Base Path", default="/tmp/")

    def scene_name(self, x, y):
        return "scene_"+str(x) +"_" + str(y)
    
    def camera_name(self, x, y):
        return "camera_"+str(x) + "_"+str(y)


    def create_scenes(self, context):
        for x in range(self.horizontal):
            for y in range(self.vertical):
                if self.scene_name(x,y) not in bpy.data.scenes:
                    bpy.ops.scene.new(type="LINK_OBJECTS") 
                    bpy.context.scene.name = self.scene_name(x,y)
                
    def create_cameras(self, context):
        center = Vector(self.center)
        hs = Vector(self.horizontal_step)
        vs = Vector(self.vertical_step)
        current = center - self.horizontal*hs/2. - self.vertical*vs/2.
        for x in range(self.horizontal):
            for y in range(self.vertical):
                bpy.context.screen.scene = bpy.data.scenes[self.scene_name(x,y)]
                if self.camera_name(x,y) in bpy.data.objects:
                    bpy.data.objects[self.camera_name(x,y)].location = current
                    bpy.data.objects[self.camera_name(x,y)].rotation_euler = (3.14 / 180.0) * Vector(self.direction)
                else:
                    bpy.ops.object.camera_add(location=current, rotation = (3.14 / 180.0) * Vector(self.direction))
                    bpy.context.selected_objects[0].name=self.camera_name(x,y)

                bpy.context.scene.camera = bpy.data.objects[self.camera_name(x,y)]
                current = current + vs
            current -= self.vertical*vs
            current = current + hs

    def create_render_layer(self, context, nodes, x, y):
        render_layers = nodes.new("CompositorNodeRLayers")
        file_output = nodes.new("CompositorNodeOutputFile")
        file_output.base_path = self.base_path + "/" +  self.camera_name(x,y)+"/"
        render_layers.scene = bpy.data.scenes[self.scene_name(x,y)]
        bpy.context.scene.node_tree.links.new(render_layers.outputs['Image'], file_output.inputs['Image'])

    def create_node_tree(self, context):
        bpy.context.screen.scene = bpy.data.scenes["Scene"]
        bpy.context.scene.use_nodes = True
        nodes = bpy.context.scene.node_tree.nodes
        for x in range(self.horizontal):
            for y in range(self.vertical):
                self.create_render_layer(context, nodes, x, y)


    def execute(self, context):        # execute() is called by blender when running the operator.
        self.create_scenes(context)
        self.create_cameras(context)
        self.create_node_tree(context)

        # The original script

        return {'FINISHED'}            # this lets blender know the operator finished successfully.

def register():
    bpy.utils.register_class(LightfieldVideo)


def unregister():
    bpy.utils.unregister_class(LightfieldVideo)


# This allows you to run the script directly from blenders text editor
# to test the addon without having to install it.
if __name__ == "__main__":
    register()

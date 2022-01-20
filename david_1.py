import bpy

bl_info = {
    "name": "David 1",
    "author": "Erik Palencik",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Lod analyzer",
    "description": "Does a lot of shit",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}


class EnableDisableAutoSmoothOperator(bpy.types.Operator):
    bl_idname = "david.enable_disable_autosmooth"
    bl_label = "Smooth control"
    bl_options = {'REGISTER', 'UNDO'}

    status:  bpy.props.BoolProperty(
        name="enable", default=True)

    smoothLevel = bpy.props.IntProperty("smoothPower", default=30)

    def execute(self, context):

        for obj in bpy.context.selected_objects:
            data: bpy.types.Mesh = obj.data
            data.use_auto_smooth = self.status

        return {'FINISHED'}


class DavidCisticOperator(bpy.types.Operator):
    bl_idname = "david.cistic"
    bl_label = "David Cistic"
    bl_options = {'REGISTER', 'UNDO'}

    container:  bpy.props.StringProperty(
        name="container", default="vertex_colors")

    def execute(self, context):

        if self.container == "vertex_groups":
            for obj in bpy.context.selected_objects:
                obj.vertex_groups.clear()
        elif self.container == "shape_keys":
            for obj in bpy.context.selected_objects:
                obj.shape_key_clear()
        elif self.container == "face_maps":
            for obj in bpy.context.selected_objects:
                obj.face_maps.clear()
        else:
            for obj in bpy.context.selected_objects:
                data: bpy.types.Mesh = obj.data
                colors: bpy.types.LoopColors = getattr(data, self.container)
                while colors:
                    print(colors[0])
                    colors.remove(colors[0])

        return {'FINISHED'}


class DavidMainControlPanel(bpy.types.Panel):
    bl_label = "David_panel"
    bl_idname = "david_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "David_panel"

    def draw(self, context):
        obj = context.object
        layout = self.layout

        data = [
            "vertex_groups",
            "shape_keys",
            "uv_layers",
            "vertex_colors",
            "face_maps",
        ]

        for i in data:
            operator = layout.operator('david.cistic', text=f"Delete: {i}")
            operator.container = i

        operator = layout.operator(
            'david.enable_disable_autosmooth', text=f"Enable smooth")
        operator.status = True

        operator = layout.operator(
            'david.enable_disable_autosmooth', text=f"Disable smooth")
        operator.status = False



def register():
    print("Registering David analyzer")
    bpy.utils.register_class(DavidMainControlPanel)
    bpy.utils.register_class(DavidCisticOperator)
    bpy.utils.register_class(EnableDisableAutoSmoothOperator)


def unregister():
    print("Unregistering David analyzer")
    bpy.utils.unregister_class(DavidCisticOperator)
    bpy.utils.unregister_class(DavidMainControlPanel)
    bpy.utils.unregister_class(EnableDisableAutoSmoothOperator)


# if __name__ == "__main__":
#     register()
register()

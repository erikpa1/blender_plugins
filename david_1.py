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


class ClearSplitData(bpy.types.Operator):
    bl_idname = "david.clear_split_data"
    bl_label = "Clear split data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selected_mesh_objects = [o for o in context.selected_objects if o.type == 'MESH']

        ao = context.view_layer.objects.active

        for o in selected_mesh_objects:
            context.view_layer.objects.active = o
            r = bpy.ops.mesh.customdata_custom_splitnormals_clear()
            print(o.name, r)

        # obj: bpy.types.Object
        # for obj in bpy.context.selected_objects:
        #     data: bpy.types.Mesh = obj.data
        #     data.custom
        #     bpy.ops.mesh.customdata_custom_splitnormals_clear(data)

        return {'FINISHED'}


class EnableDisableAutoSmoothOperator(bpy.types.Operator):
    bl_idname = "david.enable_disable_autosmooth"
    bl_label = "Smooth control"
    bl_options = {'REGISTER', 'UNDO'}

    status:  bpy.props.BoolProperty(
        name="enable", default=True)

    smoothLevel = bpy.props.IntProperty("smoothPower", default=30)

    def execute(self, context):

        obj: bpy.types.Object
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

        operator = layout.operator('david.clear_split_data', text="Clear split data")

        



def register():
    print("Registering David analyzer")
    bpy.utils.register_class(DavidMainControlPanel)
    bpy.utils.register_class(DavidCisticOperator)
    bpy.utils.register_class(EnableDisableAutoSmoothOperator)
    bpy.utils.register_class(ClearSplitData)


def unregister():
    print("Unregistering David analyzer")
    bpy.utils.unregister_class(DavidCisticOperator)
    bpy.utils.unregister_class(DavidMainControlPanel)
    bpy.utils.unregister_class(EnableDisableAutoSmoothOperator)
    bpy.utils.unregister_class(ClearSplitData)


# if __name__ == "__main__":
#     register()
register()

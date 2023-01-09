import bpy
import math

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


class ApplyScaleOperator(bpy.types.Operator):
    bl_idname = "david.applyscale"
    bl_label = "Scale"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        meshes = context.selected_objects

        if len(meshes) > 0:
            bpy.ops.object.transform_apply(location = False, scale = True, rotation = False)

        return {'FINISHED'}

class ApplyRotationOperator(bpy.types.Operator):
    bl_idname = "david.applyrotation"
    bl_label = "Rotation"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        
        meshes = context.selected_objects

        if len(meshes) > 0:
            bpy.ops.object.transform_apply(location = False, scale = False, rotation = True)

        return {'FINISHED'}



class SetSmoothOperator(bpy.types.Operator):
    bl_idname = "david.smooth"
    bl_label = "Smooth"
    bl_options = {'REGISTER', 'UNDO'}

    smoothValue: bpy.props.FloatProperty(
        name="smooth", default=30, min=0.0, max=180, soft_min=0.0,
        soft_max=180, step=1
    )

    def invoke(self, context, event):
        tmp = context.window_manager.invoke_props_dialog(self)

        return tmp

    def execute(self, context):
        
        meshes = context.selected_objects

        o: bpy.types.Object
        for o in meshes:
            print(o.type)
            if o.type == "MESH":
                o.data.auto_smooth_angle = math.radians(self.smoothValue)
                print("Angle: ", o.data.auto_smooth_angle)


        return {'FINISHED'}


class ClearSplitData(bpy.types.Operator):
    bl_idname = "david.clear_split_data"
    bl_label = "Clear split data"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):

        selected_mesh_objects = [
            o for o in context.selected_objects if o.type == 'MESH']

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


def setted(self, *args, **kwargs):
    print(args)
    return 0


class EnableDisableAutoSmoothOperator(bpy.types.Operator):
    bl_idname = "david.enable_disable_autosmooth"
    bl_label = "Smooth control"
    bl_options = {'REGISTER', 'UNDO'}

    status:  bpy.props.BoolProperty(
        name="enable", default=True)

    def execute(self, context):

        obj: bpy.types.Object
        for obj in bpy.context.selected_objects:
            data: bpy.types.Mesh = obj.data
            data.use_auto_smooth = self.status

        return {'FINISHED'}

    def invoke(self, context, event):
        return context.window_manager.invoke_props_dialog(self)


class DavidCisticOperator(bpy.types.Operator):
    bl_idname = "david.cistic"
    bl_label = "David Cistic"
    bl_options = {'REGISTER', 'UNDO'}

    container: bpy.props.StringProperty(
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
                if data:
                    colors: bpy.types.LoopColors = getattr(
                        data, self.container)
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

        layout.label(text="Object properties:")

        for i in data:
            operator = layout.operator('david.cistic', text=f"Delete: {i}")
            operator.container = i

        layout.separator(factor=3)

        operator = layout.operator(
            'david.clear_split_data', text="Clear split data")


        operator = layout.operator(
            'david.applyscale', text=f"Apply scale")
        
        operator = layout.operator(
            'david.applyrotation', text=f"Apply rotation")

        layout.label(text="Smoothing:")

        operator = layout.operator(
            'david.enable_disable_autosmooth', text=f"Enable smooth")
        operator.status = True

        operator = layout.operator(
            'david.enable_disable_autosmooth', text=f"Disable smooth")
        operator.status = False

        operator = layout.operator(
            'david.smooth', text=f"Set smooth")


def register():
    print("Registering David analyzer")
    bpy.utils.register_class(DavidMainControlPanel)
    bpy.utils.register_class(DavidCisticOperator)
    bpy.utils.register_class(EnableDisableAutoSmoothOperator)
    bpy.utils.register_class(ClearSplitData)
    bpy.utils.register_class(SetSmoothOperator)
    bpy.utils.register_class(ApplyScaleOperator)
    bpy.utils.register_class(ApplyRotationOperator)

def unregister():
    print("Unregistering David analyzer")
    bpy.utils.unregister_class(DavidCisticOperator)
    bpy.utils.unregister_class(DavidMainControlPanel)
    bpy.utils.unregister_class(EnableDisableAutoSmoothOperator)
    bpy.utils.unregister_class(ClearSplitData)
    bpy.utils.unregister_class(SetSmoothOperator)
    bpy.utils.unregister_class(ApplyScaleOperator)
    bpy.utils.unregister_class(ApplyRotationOperator)

# if __name__ == "__main__":
#     register()
register()
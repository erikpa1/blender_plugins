import bpy


bl_info = {
    "name": "Lod analyzer",
    "author": "Erik Palencik",
    "version": (1, 0, 0),
    "blender": (3, 0, 0),
    "location": "View3D > Sidebar > Lod analyzer",
    "description": "Analyze LOD",
    "warning": "",
    "doc_url": "",
    "category": "3D View",
}


class ObjectSelector(bpy.types.Operator):
    bl_idname = "lod.search"
    bl_label = "Search lod"
    bl_options = {'REGISTER', 'UNDO'}

    searchKey: bpy.props.StringProperty(
        name="Search",
    )

    def execute(self, context):

        print("Search started with: ", self.searchKey)

        for i in bpy.data.objects:
            i.select_set(False)

        search_key = self.searchKey

        someFound = False

        for i in bpy.data.objects.keys():
            object = bpy.data.objects[i]
            if i.find(search_key) != -1:
                if object.type == "MESH":
                    someFound = True
                object.select_set(True)
                object.hide_set(False)
            else:
                object.hide_set(True)

        if someFound:
            bpy.ops.object.mode_set(mode='EDIT')

        return {'FINISHED'}


class MainLodPanel(bpy.types.Panel):
    bl_label = "Lod panel"
    bl_idname = "lod_panel"
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "Lod analyzer"

    def draw(self, context):
        obj = context.object
        layout = self.layout

        row = layout.row()
        row.label(text="Write LOD level", icon="CUBE")
        row = layout.row()

        for i in range(0, 15):
            lod = "LOD" + str(i)
            searchbtn = layout.operator('lod.search', text=lod)
            searchbtn.searchKey = lod
            # layout.prop(searchbtn, "searchKey")


def register():
    print("Registering lod analyzer")
    bpy.utils.register_class(MainLodPanel)
    bpy.utils.register_class(ObjectSelector)


def unregister():
    print("Unregistering lod analyzer")
    bpy.utils.unregister_class(ObjectSelector)
    bpy.utils.unregister_class(MainLodPanel)


if __name__ == "__main__":
    register()

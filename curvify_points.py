import bpy, bmesh


def main(context):
    bpy.ops.object.mode_set(mode='EDIT')
    active_obj = bpy.context.active_object
    me = active_obj.data
    bm = bmesh.from_edit_mesh(me)
    
    verts = bm.verts
    edges = []
    
    lenMinusOne = len(verts) - 2
    
    bm.verts.ensure_lookup_table()
    
    for vi in range(0,lenMinusOne):
        
        new_edge = (verts[vi],verts[vi+1])
        bm.edges.new(new_edge)
        
    bmesh.update_edit_mesh(active_obj.data)
    bpy.ops.object.mode_set(mode='OBJECT')


class CurvifyPoints(bpy.types.Operator):
    """Tooltip"""
    bl_idname = "object.curvify_points"
    bl_label = "Curvify Points"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}


def register():
    bpy.utils.register_class(CurvifyPoints)


def unregister():
    bpy.utils.unregister_class(CurvifyPoints)


if __name__ == "__main__":
    register()

    # test call
    bpy.ops.object.curvify_points()

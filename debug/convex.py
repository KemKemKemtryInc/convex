# ---------------------------------------------------------------------------------------------
#  Copyright (c) 2024 KemKemKemtryInc. All rights reserved.
#  Licensed under the MIT License. See License.md in the project root for license information.
# --------------------------------------------------------------------------------------------

import numpy as np
import bpy
import bmesh
from bpy.types import Operator
from bpy.props import FloatProperty, IntProperty, EnumProperty, BoolProperty
from mathutils import Vector

import numpy as np
#
# Ellipse_Curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def ellipse_curve(param):
    t = param[0] 
    p = np.sin(t * 0.5 * np.pi)
    q = np.cos(t * 0.5 * np.pi)
    return p,q
#
# parabola_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def parabola_curve(param):
    x = param[0]
      
    p = x
    q = 1.0 - x*x
    return p,q
#
# circle_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def circle_curve(param):
    t0 = param[0]
    P  = param[1]
    Q  = param[2]

    if abs(Q) > 0.0001:
        R = P/Q
    else:
        R = 1.0
    
    Qr = 0.5*(R*R+1.0)
    Pr = 0.5*(R*R+1.0) / R
    y  = 0.5*(R*R-1.0)

    T = np.arccos((R*R - 1.0)/(R*R + 1.0))
    
    t = t0 * T 
    p = Pr * np.sin(t)
    q = Qr * np.cos(t) - y

    return p,q
#
# cos_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def cos_curve(param):
    t = param[0]
    p = t
    q = float(np.cos(0.5*t*np.pi))
    return p,q
#
# cos3_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def cos3_curve(param):
    t = param[0]
    p = t
    q = float(np.cos(0.5*t*np.pi)**3)
    return p,q
#
# asteroid_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
def asteroid_curve(param):
    t = param[0]
    p = (np.sin(t * np.pi*0.5))**3.0
    q = (np.cos(t * np.pi*0.5))**3.0
    return p,q
#
# gaussian_curve
#  t : Parametric variable (0～1.0)
# return 
#  p p-axis bottom point direction
#  q q-axis Apex direction
#def gaussian_curve(param):
#    t = param[0]
#    d = param[3]
#
#    p = t
#    r = 0
#    if d > 0:
#        r = np.log(1.0/(1.0+d))*t*t
#    q = float(np.exp(r))
#    return p,q
#
# 3dカーソルのローカル座標を計算する。
#
def get_3Dcursor_LocalPostion():
    # グローバル座標の3Dカーソルの位置を取得する
    gpos = bpy.context.scene.cursor.location
    g3DC_mat = np.array([gpos[0], gpos[1], gpos[2], 1.0])

    # グローバル座標に変換する行列を取得
    gmat= np.array(bpy.context.active_object.matrix_world)

    # 3Dカーソルの位置を算出する。
    g3Dcursor_localPos = np.linalg.inv(gmat).dot(g3DC_mat)
    #print("3D Cursor:", g3Dcursor_localPos)

    # ローカル座標からグローバル座標に変換する行列を取得する。
    return Vector((g3Dcursor_localPos[0], g3Dcursor_localPos[1], g3Dcursor_localPos[2]))
#
# 選択しているメッシュ(１面)を取得する。
# 2面以上選択している場合はエラー
#
def get_selected_face(b_mesh):
    # 選択されたサーフェスを取得
    selected_F = [F for F in b_mesh.faces if F.select]
    
    selF = None
    isOK = True
    # 選択しているサーフェースの数をチェック 
    if len(selected_F) != 1 :
        #raise Exception("Not Selected serface.")
        isOK = False
    else:
        selF = selected_F[0]
    
    return selF, isOK
#
# 選択している面以外の選択している点を取得する。
#
def get_selected_apex_vert(b_mesh, selF):
    # 選択された点(選択面の点も含む)
    selected_V = [V for V in b_mesh.verts if V.select]

    selV   = None
    indexV = None
    for j in range(len(selected_V)):           # 選択した点（サーフェースの点も含む)
        isBreak = False
        for i in range(len(selF.verts)):       # 選択したサーフェースの点
            if selected_V[j].index == selF.verts[i].index:
                isBreak = True
                break
        if isBreak == False:
            indexV = j
            break

    if (indexV != None):
        selV = selected_V[indexV].co

    return selV
# 
#  サーフェスの法線ベクトルと重心を計算する。
#
def calc_average_normal(selF):
    #サーフェスの重心を計算
    poslist = [V.co for V in selF.verts]
    gom = np.sum(poslist, axis=0) / len(poslist)

    #重心を原点とする。
    q = poslist - gom
    # 3x3行列を計算する 行列計算で和の形になるため総和になる
    Q = np.dot(q.T, q)
    # 固有値、固有ベクトルを計算　固有ベクトルは縦のベクトルが横に並ぶ形式
    la, vectors = np.linalg.eig(Q)
    # 固有値が最小となるベクトルの成分を抽出
    normal = vectors.T[np.argmin(la)]
    
    #サーフェースの平均法線ベクトル
    vnormal = Vector(t for t in normal)
    #サーフェースの重心
    vgom    = Vector(t for t in gom)
    return vnormal, vgom

# MESH_OT_add_helix
# turns:
# radius:
# height:
class MESH_OT_add_convex(Operator):
    bl_idname = "mesh.add_convex_surface"
    bl_label = "凸型のサーフェースを追加します。"
    bl_options = {'REGISTER', 'UNDO'}

    apex      = None          # 頂点      
    selectedF = None          # 選択サーフェス
    normal = Vector()         # サーフェスの法線ベクトル
    gom = Vector()            # サーフェスの重心
    pq_o = Vector()           # P-Q座標の原点
    
    functionType: EnumProperty(
        name="断面曲線",
        description="断面曲線を選択",
        items=[
            ('ellipse_curve', "ellipse", "Set ellipse"),
            ('parabola_curve', "parabola", "Set parabola"),
            ('circle_curve', "circle", "Set circle"),
            ('cos_curve', "cos", "Set cos"),
            ('asteroid_curve',"asteroid","set asteroid"),
            ('cos3_curve',"cos^3","set cos^3")
        ],
        default='ellipse_curve'
    )

    segment: IntProperty(
        name="分割数",
        description="サーフェースの分割数",
        default=8,
        min=1
    )

    apexPointType: EnumProperty(
        name="頂点",
        description="頂点の指定方法を点または髙さで指定します。",
        items=[
            ('ITEM_HEIGHT', "髙さ指定", "Set Hight"),
            ('ITEM_3DCURSOR', "3Dカーソル", "3D Cursor"),
            ('ITEM_SEL_POINT', "選択点", "Selected Point")
        ],
        default='ITEM_SEL_POINT'
    )

    height: FloatProperty(
        name="頂点の高さ",
        description="Height to apex",
        default=1.0,
        min=-1000.0,
        max=1000.0
    )

    mergeTpoint: BoolProperty(
        name="頂点をマージ",
        description="頂点をマージします。",
        default=True
    )
    
    apexExtentRatio: FloatProperty(
        name="頂点の広がり",
        description="Apex expanse",
        default=0.0,
        min=0.0,
        max=10.0
    )
    
    apexHRatio: FloatProperty(
        name="上面の高さ",
        description="Apex height offset",
        default=0.0,
        min=-10.0,
        max=10.0
    )

    #
    # 髙さと法線ベクトルから頂点を計算する。
    #
    def calc_apex_vert(self):
        apex = self.gom + self.height * self.normal
        
        # 単位調整
        # bpy.context.scene.unit_settings.length_unit = 'METERS'
        # 頂点を追加
        return apex
    #
    # 頂点座標,p-q座標の原点を計算
    #
    def get_apex_vert(self, b_mesh):
        apexV = None     # 頂点座標
        pq_o = None     # p-q座標の原点

        # 選択点,3DCursorの場合
        if (self.apexPointType == 'ITEM_SEL_POINT'):
            apexV = get_selected_apex_vert(b_mesh, self.selectedF)
        elif (self.apexPointType == 'ITEM_3DCURSOR'):
            apexV = get_3Dcursor_LocalPostion()
            #print("3D Point", apexV)

        if (self.apexPointType == 'ITEM_HEIGHT' or apexV==None):
            apexV = self.calc_apex_vert()
            pq_o = self.gom      # 選択したサーフェスの重心
            self.apexPointType = 'ITEM_HEIGHT'
        else:
            # p-q座標の原点
            n_gt   = apexV - self.gom
            t      = n_gt.dot(self.normal)
            pq_o   = apexV - t * self.normal

        #print("---base point---")
        #print(self.pq_o)

        return apexV, pq_o
    #
    #  点を平面に移動する。 
    #    Input
    #    pos    : selected point postion.
    #    normal : normal vector
    #    center : center point postion
    #
    def point_onto_plane(self, pos, normal, center):
        n = np.dot(normal, normal)
        d = np.dot(center, normal)
        l = np.dot(pos, normal)
        t = (d - l) / n
        
        newPos =  t * normal + pos
        newPosV = Vector(t for t in newPos)
        return newPosV
    #
    # サーフェスを追加する
    #
    def add_face(self, b_mesh, point):
        newF = None
        # 選択面のmaterialを取得
        # faces[] 
        #   p0 ←  P3
        #    ↓    ↑ 
        #   p1 →  p2
        if (point[0] == point[3]):
            point3 = [point[0], point[1], point[2]]
            newF = b_mesh.faces.new(point3)
            print(point)
        elif (point[1] == point[2]):
            point3 = [point[0], point[2], point[3]]
            newF = b_mesh.faces.new(point3)
            print(point)
        else:
            newF = b_mesh.faces.new(point)
    
        newF.material_index = self.selectedF.material_index
        return
    #
    #
    #
    def add_covex_mesh(self, b_mesh, Curve_f):
        
        vertslist = []    
        b_mesh.verts.ensure_lookup_table()
        b_mesh.faces.ensure_lookup_table()
        point = [None,None,None,None]   # 新しいサーフェスの4verts
        pos3D = Vector()                # Curve_f上の3D座標
        for n in range(self.segment+1):
            for i in range(len(self.selectedF.verts)):
                selF_ver = self.selectedF.verts[i].co      # 選択面の1点

                #頂点をOFFSET
                flattenF = self.point_onto_plane(selF_ver, self.normal, self.gom)
                flattenF_ver = (1.0 - self.apexHRatio) * flattenF + self.apexHRatio * selF_ver
                offsetV = self.apexExtentRatio * (flattenF_ver - self.gom)
                offset_apex  = self.apex + offsetV
                offset_pq_o = self.pq_o + offsetV

                # q方向の長さ
                qLen = (offset_apex - offset_pq_o).length   # 頂点までの髙さ

                # p方向の長さ
                pLen = (selF_ver - offset_pq_o).length     # p-q原点からサーフェス上の点までの距離

                t = n / self.segment 
                                
                # 断面座標系(p,q)の曲線上の点
                param = [t, pLen, qLen, self.segment] 
                p,q = Curve_f(param)

                # 断面座標系(p,q)を3D座標系に変換
                pos3D = p * (selF_ver - offset_pq_o) + q * (offset_apex - offset_pq_o) + offset_pq_o

                if n == 0:
                    # 頂点を追加
                    if self.mergeTpoint == True:
                        # 頂点は１点追加し他はその参照
                        if (len(vertslist)==0):
                            vertslist.append(b_mesh.verts.new(pos3D)) #1点を作成
                        else:
                            vertslist.append(vertslist[0]) #その他は参照
                    else:
                        # 頂点を逐次追加する。
                        vertslist.append(b_mesh.verts.new(pos3D))
                else:

                    if n == self.segment:
                        point[2] = self.selectedF.verts[i] # 底面は選択点にする。
                    else:
                        point[2] = b_mesh.verts.new(pos3D)
                    point[3] = vertslist[i]
                
                    if (i == 0):
                        sPoint = vertslist[0]
                    else:
                        # サーフェスを追加
                        self.add_face(b_mesh, point)

                    vertslist[i] = point[2]
                    point[0] = point[3]
                    point[1] = point[2]
    
            # ループ1周したとき、最後の点と最初の点でサーフェスを作る。
            if n > 0:
                point[2] = vertslist[0]
                point[3] = sPoint
                self.add_face(b_mesh, point)
            
        b_mesh.normal_update()

        return
    #
    # execute
    #
    def execute(self, context):
        if bpy.context.mode != 'EDIT_MESH':
            return {'False'}
        
        # カレントのメッシュを取得
        bpy.context.edit_object.update_from_editmode()

        # Get active Object
        obj = bpy.context.active_object
        mesh = obj.data
        # Get a BMesh representation
        b_mesh = bmesh.from_edit_mesh(mesh)

        # 選択ポリゴンを取得
        self.selectedF, isCalcOK = get_selected_face(b_mesh)
        if isCalcOK == False:
            return {'CANCELLED'}
                
        # 選択面の法線ベクトルと重心を計算する。
        self.normal, self.gom = calc_average_normal(self.selectedF)
        #print(self.normal)
        #print(self.gom)

        if self.normal.length < 0.0001:
            raise Exception("Incorrect normal vector.")

        if self.mergeTpoint == True:
            self.apexExtentRatio = 0.0
            self.apexHRatio      = 1.0

        # 頂点を生成とpq座標の原点座標を計算
        self.apex, self.pq_o = self.get_apex_vert(b_mesh)
        #print("--- apexPoint ----------")
        #print(self.apex)
        #print("--- select Face verts num----------")
        #print(len(self.selectedF.verts))

        #断面曲線からメッシュを貼る
        self.add_covex_mesh(b_mesh, eval(self.functionType))

        bmesh.update_edit_mesh(mesh)
        b_mesh.free()

        return {'FINISHED'}

#
#  UIの表示
#    
    def draw(self, context):
        layout = self.layout
        
        #layout.prop(self, "functionType", expand=True)
        layout.prop(self, "functionType")
        layout.separator()
        layout.prop(self, "segment")

        layout.separator()
        layout.prop(self, "apexPointType")

        col1 = layout.column()
        col1.prop(self, "height")
        if self.apexPointType == 'ITEM_HEIGHT':
            col1.enabled = True
        else:
            col1.enabled = False

        layout.separator()
        layout.prop(self, "mergeTpoint")

        col2 = layout.column()
        col2.prop(self, "apexExtentRatio")
        col2.prop(self, "apexHRatio")
        if self.mergeTpoint == True:
            self.apexExtentRatio = 0.0
            self.apexHRatio = 0.0
            col2.enabled = False
        else:
            col2.enabled = True

def menu_func(self, context):
    layout = self.layout
    layout.separator()
    layout.operator_context = "INVOKE_DEFAULT"
    #layout.operator(convex.MESH_OT_add_convex.bl_idname, text="Add Convex surface")
    layout.operator(MESH_OT_add_convex.bl_idname, text="Add Convex Surface")

def register():    
    bpy.utils.register_class(MESH_OT_add_convex)
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.append(menu_func)


def unregister():
    bpy.types.VIEW3D_MT_edit_mesh_context_menu.remove(menu_func)
    bpy.utils.unregister_class(convex.MESH_OT_add_convex)
  
if __name__ == "__main__": 
    register()


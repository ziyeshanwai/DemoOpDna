# _*_ coding: utf-8 _*_
# @FileName:modifyDnaDeltaBlendshapes
# @Date:2024-09-18:14:
# @Auther: liyou wang
# @Contact: matrix2@foxmail.com

import os
import dna
import numpy as np
import shutil
import json


def save_dict_to_json(data, filename):
    """
    将字典保存为JSON文件

    :param data: 需要保存的字典
    :param filename: 保存的文件名
    """
    try:
        # 打开文件并写入字典数据
        with open(filename, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, ensure_ascii=False, indent=4)
        print(f"字典数据成功保存到 {filename}")
    except Exception as e:
        print(f"保存时发生错误: {e}")


class ModifyDeltaBSDna:

    def __init__(self, input_dna_path, output_dna_path):
        self._dna_path = input_dna_path
        self._output_dna_path = output_dna_path
        if os.path.isfile(self._dna_path):
            shutil.copy2(self._dna_path, self._output_dna_path)
        stream = dna.FileStream(self._output_dna_path, dna.FileStream.AccessMode_Read, dna.FileStream.OpenMode_Binary)
        self._reader = dna.BinaryStreamReader(stream, dna.DataLayer_All)
        self._reader.read()
        stream = dna.FileStream(self._output_dna_path, dna.FileStream.AccessMode_Write, dna.FileStream.OpenMode_Binary)
        self._writer = dna.BinaryStreamWriter(stream)
        self._writer.setFrom(self._reader)

        # self._writer.write()

    def _add_blendshape(self):
        # mesh_count = self._reader.getMeshCount()
        # 5 6 7 eye_look_up eye_look_down eye_look_left eye_look_right eye_blink
        # for i in range(0, mesh_count):
        #     mesh_name = self._reader.getMeshName(i)
        names = []
        blend_shape_channel_index = [j for j in range(60, 92)]
        extenal_index = [30, 31, 34, 35, 36, 37, 38, 39]
        for i in extenal_index:
            blend_shape_channel_index.append(i)
        start = self._reader.getMeshBlendShapeChannelMappingCount()
        for i in [5, 6, 7]:
            mesh_name = self._reader.getMeshName(i)
            for n, j in enumerate(blend_shape_channel_index):
                bs_name = self._reader.getBlendShapeChannelName(n)
                self._writer.setBlendShapeChannelIndex(i, n, j)
                self._writer.setBlendShapeTargetDeltas(i, n, [[0, 0, 0.0001]])
                self._writer.setBlendShapeTargetVertexIndices(i, n, [0])
                self._writer.setMeshBlendShapeChannelMapping(start, i, j)
                start += 1
                names.append("{}__{}".format(mesh_name, bs_name))

        # self._writer.setBlendShapeChannelIndex(7, 5, 31)  # eye_blink_R
        # self._writer.setBlendShapeTargetDeltas(7, 5, [[0, 0, 0]])
        # self._writer.setBlendShapeTargetVertexIndices(7, 5, [0])
        # ori_morph_num = len(self._reader.getBlendShapeChannelIndicesForLOD(0))
        # ind = [i for i in range(0, ori_morph_num + 3 * len(blend_shape_channel_index))]
        # self._writer.setMeshBlendShapeChannelMapping()
        # self._writer.setLODBlendShapeChannelMapping(0, ori_morph_num + 3 * len(blend_shape_channel_index))
        # self._writer.setMeshBlendShapeChannelMapping()
        # self._writer.setBlendShapeChannelIndices()
        # self._writer.setBlendShapeChannelInputIndices()
        curve = {}
        curve['curve_data'] = names
        self._writer.write()
        save_dict_to_json(curve, "./curves_name.json")

    def run(self):
        self._add_blendshape()
        # pass


if __name__ == "__main__":
    input_dna = r"./head.dna"
    output_dna = r"./head_o.dna"
    mdb = ModifyDeltaBSDna(input_dna, output_dna)
    mdb.run()


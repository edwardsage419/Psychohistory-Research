# v3.2 自主认知专项第19轮（累计第78轮）：外部语言数据来源、资源预算及完整版本准备度

2026-11-25。RESEARCH_CANDIDATE / SOURCE_METADATA_VERIFIED / RESOURCE_FORMULA_EXECUTED / RAW_DATA_NOT_ACQUIRED / TRAINING_NOT_AUTHORIZED。实际main 20c8df044c3a4d48f1819a7f401901d5ecde7a3e，13开放Draft PR，#61 head 4c133cd2eed4d5c5f0f164aca1efa2b07cdabf9e。核查最近8提交、未截断Git树相关路径、v3.2 7cee2ec8e740ef3b89c0b5d4b2fc7336fac19b85（前段及历史全文）、AGENTS 78cc1f8327ec50b5762103fedfaf1f06e85f7658、同步规程26c4d946e48f01858fb8e8c2cb06e4f7ba91bf05、唯一交接5e74f4f0b37141d631740e844ad8bbbfed232e07（相关标题，非全文）、R72 82f53eb20bcb7b49e0e56088a7c2c586000627fa、R50 4d394d2cb6e1e1dfc667f2a8806f896a36bbdbef、R77 16075b3ba567ee6dc3496300beab1417172a6c42。既有两套32情节64轮167条标注均为公开原创合成开发资料，不作独立留出或未经授权的训练。R77原始双轮文本全边候选12/12覆盖但首位3/12，停止重复扩大固定词面枚举。本轮新增外部来源及版本登记、静态参数与计算规模复算、完整版本条件更新；不执行训练、原生产品或独立验收。

## 外部来源（仅英文公开资料及固定GitHub文件）
1. Universal Dependencies Chinese GSDSimp 官方 https://universaldependencies.org/treebanks/zh_gsdsimp/ 显示CC BY-SA 4.0、wiki体裁、4997句123289词元；繁转简及人工修订，词性/关系等标注由既有人工标注转换、部分自动修正。实际核对官方统计页以及固定Git README与LICENSE；README特别说明Google同意取消NC的范围为UD标注，底层文本权利另核对。不能把当前官方统计自动绑定固定commit的字节或推断全部内容适合训练。固定Git目录给出三个文件大小及blob，合计11653019字节（仅元数据）；尝试读取dev第1..120行返回空内容，未获得数据正文或本地SHA256、未解析词元、未验证实际划分和泄漏。适合句法/分词基础候选；不代表对话义务。
2. MASSIVE: FitzGerald et al. ACL 2023 https://aclanthology.org/2023.acl-long.235/ 及作者机构 https://www.amazon.science/blog/amazon-releases-51-language-dataset-for-language-understanding ：专业翻译者从英语SLURP本地化，原1.0为51语言，1.1为52语言，60意图55槽位；数据CC BY 4.0，包含zh-CN。实际读英文摘要、作者机构说明、固定Git README（1.1其他语言与1.0相同的发布声明、JSONL格式utt/annot_utt）；未取得1.1包内LICENSE、字节、中文数据量或样本。代码许可证不替代数据许可。适合意图/槽位及数量语言候选，翻译来源、单轮助手命令与真实个人决策分布差异明显；所有平行语言共享原始语义ID，必须按源情节分组，禁止跨语言泄漏。
3. CrossWOZ: Zhu et al. TACL 2020 https://aclanthology.org/2020.tacl-1.19/ DOI 10.1162/tacl_a_00314；论文摘要6000对话约102000话语、5领域（酒店/餐饮/景点/地铁/出租车），约60%跨领域目标；Wizard-of-Oz有任务设定，不是自由生活决策的真实自然分布。实际读论文摘要、固定README（对话状态、对话行为、双人同步标注说明、annotator ID字段）、仓库Apache-2.0标记及目录元数据。未读取固定LICENSE正文、数据文件许可范围与参与者同意，未获取原始对话。GEM镜像元数据 https://huggingface.co/datasets/GEM/CrossWOZ/blob/main/dataset_infos.json 声明Apache-2.0，但镜像数量及挑战集未复算，不能代替源许可。后续分离标注者ID与内容，避免个人资料或重新识别；按完整对话、共同任务模板及来源分组。适合多轮状态跟踪与跨域引用辅助，不能将任务slot直接映射为本人硬底线或权威事实。

上述三者全部仅来源候选、无实际训练准入、无完整原始数据哈希或实际内容审查。当前不复制文本或下载包到公开仓库，不宣称取得合格训练集；先固定具体许可和来源链、用途/再分发/派生模型适用条件，保留署名及相同方式共享等义务，法律不确定则保留阻断。三者与原始真实生活决策语料分层；不可用语料生成真实效果证据。文献只读摘要及作者文档，未分析PDF全文或复现原论文。
```json
[
  {
    "id": "UD_GSDSIMP",
    "repo": "UniversalDependencies/UD_Chinese-GSDSimp",
    "ref": "b79a1c2f7ba7f9b264808d91c6886a67b7f847a3",
    "readme": "5cb7d4a8446b4a167915225483aa94d187f23798",
    "licenseBlob": "9af2e0b2f73cf29fe1f60cb6376b176d9c2ba846",
    "license": "CC BY-SA 4.0 (treebank; underlying wiki content rights separately verify)",
    "official": "https://universaldependencies.org/treebanks/zh_gsdsimp/",
    "files": [
      {
        "name": "zh_gsdsimp-ud-train.conllu",
        "bytes": 9321026,
        "blob": "bba817038c0745be1f3c904597d56dea6422383f"
      },
      {
        "name": "zh_gsdsimp-ud-dev.conllu",
        "bytes": 1195378,
        "blob": "af8cc878e7934b38ce3c1a266053100e7c47de6f"
      },
      {
        "name": "zh_gsdsimp-ud-test.conllu",
        "bytes": 1136615,
        "blob": "4e0ba003ca267a21857185c73c2cab755ab6fe4f"
      }
    ],
    "status": "METADATA_ONLY; connector requested lines 1..120 dev returned empty content"
  },
  {
    "id": "CROSSWOZ",
    "repo": "thu-coai/CrossWOZ",
    "ref": "df82c9fdff91b9b130f2d6b89110d3870ba6260e",
    "readme": "6edbb651085d6f5f3ed2f0e712bc5493d0e78745",
    "licenseBlob": "261eeb9e9f8b2b4b0d119366dda99c6fd7d35c64",
    "license": "repository Apache-2.0; data-specific scope and collection terms require review",
    "official": "https://aclanthology.org/2020.tacl-1.19/",
    "dataTree": "d2365fbcdb4d81ddf42bc01bdb845adfb1b7eea0",
    "status": "METADATA_ONLY"
  },
  {
    "id": "MASSIVE",
    "repo": "alexa/massive",
    "ref": "f966f21846043aabef9b0f974fa7970027f43738",
    "readme": "eb03f1f03985b648bd62c191d262e466dec73b83",
    "licenseBlob": "05d304f13420c406ba1ec437790809f53c2558a5",
    "license": "data CC BY 4.0 per Amazon Science; separate code license; archive-specific LICENSE not obtained",
    "official": "https://www.amazon.science/blog/amazon-releases-51-language-dataset-for-language-understanding",
    "archive": "https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz",
    "status": "METADATA_ONLY"
  }
]
```

## 资源候选预算（静态计算，不是实测设备速度）
承接R75部分监督CRF数学；仅3标签的独立BIO头数H、每头共享特征词表大小F、每位置活动特征16、float32、长度T。参数 H(3F+9)，权重4字节/参数，Adam权重/梯度/一阶/二阶四数组最低16字节/参数；局部发射稀疏乘加 H*T*16*3，单次前向转移上界 H*T*9，前后向两次 H*T*18（不含期望梯度累积、特征提取和数值运算细节）。全前后向alpha/beta数组估算2*H*T*3*4字节。不等于整体内存、训练时间、硬件性能、模型能力或费用；稀疏特征字典、框架、优化器其他缓存、数据、batch、解析图与推理均另计。H=3/20、F=10000/50000/200000、T=64/128/512共18个候选预算，3项公式检查实际执行。3/20头仅探索规模，非确定架构；20个角色不意味着必须20个独立头，更不保证语义质量。以低资源实验候选优先，不使用或下载第三方预训练权重；训练需要单独授权和实际设备测量。不凭理论数组规模承诺iPhone可运行。
```js
function budget(){
 const cases=[];for(const F of [10000,50000,200000])for(const H of [3,20])for(const T of [64,128,512]){
  const K=3,B=4,active=16;
  // H independent BIO heads; emission table F x K per head; separate dense transitions.
  const p=H*(F*K+K*K),weightBytes=p*B;
  cases.push({featureVocabulary:F,heads:H,length:T,parameters:p,float32WeightBytes:weightBytes,float32AdamLowerBoundBytes:4*weightBytes,emissionMultiplyAdds:H*T*active*K,forwardTransitionUpperBound:H*T*K*K,forwardBackwardTransitionUpperBound:2*H*T*K*K,fullAlphaBetaFloat32Bytes:2*H*T*K*B});
 }
 const ck=(x,m)=>{if(!x)throw Error(m)};
 ck(cases.length===18,"grid");
 ck(cases.every(x=>x.float32WeightBytes===4*x.parameters&&x.float32AdamLowerBoundBytes===16*x.parameters),"bytes");
 ck(cases.every(x=>x.forwardBackwardTransitionUpperBound===2*x.forwardTransitionUpperBound),"passes");
 const selected=cases.filter(x=>x.length===128);
 return {cases,selected,controls:3,assumptions:{labelsPerHead:3,activeFeaturesPerPosition:16,bytesPerFloat32:4,adamArrays:4,exclude:"feature dictionary, tokenization, model metadata, runtime, intermediate activations, allocator, batching, training data, framework overhead, real device performance"}};
}
```
```json
{
  "cases": [
    {
      "featureVocabulary": 10000,
      "heads": 3,
      "length": 64,
      "parameters": 90027,
      "float32WeightBytes": 360108,
      "float32AdamLowerBoundBytes": 1440432,
      "emissionMultiplyAdds": 9216,
      "forwardTransitionUpperBound": 1728,
      "forwardBackwardTransitionUpperBound": 3456,
      "fullAlphaBetaFloat32Bytes": 4608
    },
    {
      "featureVocabulary": 10000,
      "heads": 3,
      "length": 128,
      "parameters": 90027,
      "float32WeightBytes": 360108,
      "float32AdamLowerBoundBytes": 1440432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 10000,
      "heads": 3,
      "length": 512,
      "parameters": 90027,
      "float32WeightBytes": 360108,
      "float32AdamLowerBoundBytes": 1440432,
      "emissionMultiplyAdds": 73728,
      "forwardTransitionUpperBound": 13824,
      "forwardBackwardTransitionUpperBound": 27648,
      "fullAlphaBetaFloat32Bytes": 36864
    },
    {
      "featureVocabulary": 10000,
      "heads": 20,
      "length": 64,
      "parameters": 600180,
      "float32WeightBytes": 2400720,
      "float32AdamLowerBoundBytes": 9602880,
      "emissionMultiplyAdds": 61440,
      "forwardTransitionUpperBound": 11520,
      "forwardBackwardTransitionUpperBound": 23040,
      "fullAlphaBetaFloat32Bytes": 30720
    },
    {
      "featureVocabulary": 10000,
      "heads": 20,
      "length": 128,
      "parameters": 600180,
      "float32WeightBytes": 2400720,
      "float32AdamLowerBoundBytes": 9602880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    },
    {
      "featureVocabulary": 10000,
      "heads": 20,
      "length": 512,
      "parameters": 600180,
      "float32WeightBytes": 2400720,
      "float32AdamLowerBoundBytes": 9602880,
      "emissionMultiplyAdds": 491520,
      "forwardTransitionUpperBound": 92160,
      "forwardBackwardTransitionUpperBound": 184320,
      "fullAlphaBetaFloat32Bytes": 245760
    },
    {
      "featureVocabulary": 50000,
      "heads": 3,
      "length": 64,
      "parameters": 450027,
      "float32WeightBytes": 1800108,
      "float32AdamLowerBoundBytes": 7200432,
      "emissionMultiplyAdds": 9216,
      "forwardTransitionUpperBound": 1728,
      "forwardBackwardTransitionUpperBound": 3456,
      "fullAlphaBetaFloat32Bytes": 4608
    },
    {
      "featureVocabulary": 50000,
      "heads": 3,
      "length": 128,
      "parameters": 450027,
      "float32WeightBytes": 1800108,
      "float32AdamLowerBoundBytes": 7200432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 50000,
      "heads": 3,
      "length": 512,
      "parameters": 450027,
      "float32WeightBytes": 1800108,
      "float32AdamLowerBoundBytes": 7200432,
      "emissionMultiplyAdds": 73728,
      "forwardTransitionUpperBound": 13824,
      "forwardBackwardTransitionUpperBound": 27648,
      "fullAlphaBetaFloat32Bytes": 36864
    },
    {
      "featureVocabulary": 50000,
      "heads": 20,
      "length": 64,
      "parameters": 3000180,
      "float32WeightBytes": 12000720,
      "float32AdamLowerBoundBytes": 48002880,
      "emissionMultiplyAdds": 61440,
      "forwardTransitionUpperBound": 11520,
      "forwardBackwardTransitionUpperBound": 23040,
      "fullAlphaBetaFloat32Bytes": 30720
    },
    {
      "featureVocabulary": 50000,
      "heads": 20,
      "length": 128,
      "parameters": 3000180,
      "float32WeightBytes": 12000720,
      "float32AdamLowerBoundBytes": 48002880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    },
    {
      "featureVocabulary": 50000,
      "heads": 20,
      "length": 512,
      "parameters": 3000180,
      "float32WeightBytes": 12000720,
      "float32AdamLowerBoundBytes": 48002880,
      "emissionMultiplyAdds": 491520,
      "forwardTransitionUpperBound": 92160,
      "forwardBackwardTransitionUpperBound": 184320,
      "fullAlphaBetaFloat32Bytes": 245760
    },
    {
      "featureVocabulary": 200000,
      "heads": 3,
      "length": 64,
      "parameters": 1800027,
      "float32WeightBytes": 7200108,
      "float32AdamLowerBoundBytes": 28800432,
      "emissionMultiplyAdds": 9216,
      "forwardTransitionUpperBound": 1728,
      "forwardBackwardTransitionUpperBound": 3456,
      "fullAlphaBetaFloat32Bytes": 4608
    },
    {
      "featureVocabulary": 200000,
      "heads": 3,
      "length": 128,
      "parameters": 1800027,
      "float32WeightBytes": 7200108,
      "float32AdamLowerBoundBytes": 28800432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 200000,
      "heads": 3,
      "length": 512,
      "parameters": 1800027,
      "float32WeightBytes": 7200108,
      "float32AdamLowerBoundBytes": 28800432,
      "emissionMultiplyAdds": 73728,
      "forwardTransitionUpperBound": 13824,
      "forwardBackwardTransitionUpperBound": 27648,
      "fullAlphaBetaFloat32Bytes": 36864
    },
    {
      "featureVocabulary": 200000,
      "heads": 20,
      "length": 64,
      "parameters": 12000180,
      "float32WeightBytes": 48000720,
      "float32AdamLowerBoundBytes": 192002880,
      "emissionMultiplyAdds": 61440,
      "forwardTransitionUpperBound": 11520,
      "forwardBackwardTransitionUpperBound": 23040,
      "fullAlphaBetaFloat32Bytes": 30720
    },
    {
      "featureVocabulary": 200000,
      "heads": 20,
      "length": 128,
      "parameters": 12000180,
      "float32WeightBytes": 48000720,
      "float32AdamLowerBoundBytes": 192002880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    },
    {
      "featureVocabulary": 200000,
      "heads": 20,
      "length": 512,
      "parameters": 12000180,
      "float32WeightBytes": 48000720,
      "float32AdamLowerBoundBytes": 192002880,
      "emissionMultiplyAdds": 491520,
      "forwardTransitionUpperBound": 92160,
      "forwardBackwardTransitionUpperBound": 184320,
      "fullAlphaBetaFloat32Bytes": 245760
    }
  ],
  "selected": [
    {
      "featureVocabulary": 10000,
      "heads": 3,
      "length": 128,
      "parameters": 90027,
      "float32WeightBytes": 360108,
      "float32AdamLowerBoundBytes": 1440432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 10000,
      "heads": 20,
      "length": 128,
      "parameters": 600180,
      "float32WeightBytes": 2400720,
      "float32AdamLowerBoundBytes": 9602880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    },
    {
      "featureVocabulary": 50000,
      "heads": 3,
      "length": 128,
      "parameters": 450027,
      "float32WeightBytes": 1800108,
      "float32AdamLowerBoundBytes": 7200432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 50000,
      "heads": 20,
      "length": 128,
      "parameters": 3000180,
      "float32WeightBytes": 12000720,
      "float32AdamLowerBoundBytes": 48002880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    },
    {
      "featureVocabulary": 200000,
      "heads": 3,
      "length": 128,
      "parameters": 1800027,
      "float32WeightBytes": 7200108,
      "float32AdamLowerBoundBytes": 28800432,
      "emissionMultiplyAdds": 18432,
      "forwardTransitionUpperBound": 3456,
      "forwardBackwardTransitionUpperBound": 6912,
      "fullAlphaBetaFloat32Bytes": 9216
    },
    {
      "featureVocabulary": 200000,
      "heads": 20,
      "length": 128,
      "parameters": 12000180,
      "float32WeightBytes": 48000720,
      "float32AdamLowerBoundBytes": 192002880,
      "emissionMultiplyAdds": 122880,
      "forwardTransitionUpperBound": 23040,
      "forwardBackwardTransitionUpperBound": 46080,
      "fullAlphaBetaFloat32Bytes": 61440
    }
  ],
  "controls": 3,
  "assumptions": {
    "labelsPerHead": 3,
    "activeFeaturesPerPosition": 16,
    "bytesPerFloat32": 4,
    "adamArrays": 4,
    "exclude": "feature dictionary, tokenization, model metadata, runtime, intermediate activations, allocator, batching, training data, framework overhead, real device performance"
  }
}
```

## 完整版本准备度和下一步（候选建议）
R50十二项完整范围保持，14个正式验收门未取得本轮新通过证据；不把研究轮数或数据规模当版本百分比。R59原生语言冷启动覆盖不够、R77跨轮排序不足、R68-71只有隔离原生数学连接，旧Qwen/Ollama条件按v3.2取消。实际缺口：(1)正式基线和支持环境仍未执行完整回归；(2)统一IR及自主候选需真实白话覆盖和独立资格；(3)外部数据实际许可/字节/安全内容/去重/分组及真实决策语言未获得；(4)独立评价及自研训练授权未获；(5)Mac/iPhone实际资源、断网、撤回、更新回退与长期反馈尚未验证。建议先完成数据获取和许可审计及独立数据分割协议，制定从零初始化模型的固定基线、学习曲线、风险评估、运行设备及资源预算，授权后才进行一次完整版本研发。候选B+C（小型统计跨度+组合语义）和简单规则比较，同等信息、未见情节、报告漏义务及错误放行、条件/单位/主体与上下文、风险和拒答、复算及实际任务时间；最终路线仍待证据决定。数据轨负责合法来源和独立隔离，产品轨唯一交接，独立轨冻结未见案例；手动窗口研究候选学习接口/复杂组合及正式运行条件，不重复数据轨同一来源。未启动训练、Codex、CI、合并、部署、生产修改或新增费用，冻结协议不变。

勘误：初次归档的三个UD文件元数据合计存在200字节转录差异；实际复算9321026+1195378+1136615=11653019。原始提交保留于Git历史，其他数据及结论不变。

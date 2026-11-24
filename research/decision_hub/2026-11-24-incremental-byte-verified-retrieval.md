# 第51轮：真实仓库文本的增量索引、字节验证与跨语言检索
2026-11-24。固定main f329664583fbce5b8d96248de2a0e5950806151a，核对v3.1、AGENTS、同步规程、近期提交、开放PR、唯一交接及第28/29/50轮。当前PR #61仍待审。第29轮config blob 3a2d448caff63dedb9638aaef1eceaf6cd70bc5f，154份固定清单；postings_sample blob 4cfc4cdab4466b40d83b629139b5cf330ffe31f2 为既有8份词频（本轮复用，未重算原字节）。本轮实际container git ls-remote再次DNS失败，无法完整本地检出；改用GitHub连接器base64分批读取此前24份之外的8份真实文件，按固定清单校验原始字节长度、Git blob SHA1（含blob头）、UTF8往返。自实现SHA1核对空串与abc标准向量。Git blob用于内容身份，不证明文献真实性或科学效力。累计历史实际正文处理32/154，122份尚未处理；本轮可共同检索16份（8旧词频、8新正文），不是32份共同检索或全库。选择新增文档涉及信息价值、沉没成本、后悔、基准率、测量、缺失数据、单人因果、预测评分；不是随机抽样。仅归档指标、来源身份和原创复算代码，不复制文献正文。未独立验证外部原论文或所有文档许可。历史固定清单不是当前全部仓库资产。
## 实验
人工10条目标检索、3条范围外问题，事前按文档题名指定目标（Q10允许两个候选），英文扩展人工提供，非真实Qwen。与第28轮不同，评价明确目标文件而非主题命中；不能直接比较准确率。BM25 k1=1.2,b=.75，中文二元组/英文词。比较文件名英文扩展、正文中文、正文中英扩展。新8份原始字节独立复核通过，旧8份复用固定posting。排名不等于证据质量、模型适用或执行授权。查询结果均authority NONE；未验证全文检索生产服务、真实用户、自然语言泛化或独立留出。
## 实际结果
```json
{
  "stats": {
    "newDocs": 8,
    "bytes": 42778,
    "tokens": 8615,
    "identityMatches": 8,
    "searchDocs": 16,
    "cumulativeRead": 32,
    "missing": 122,
    "metrics": {
      "filename_expanded": {
        "hit1": 10,
        "hit3": 10,
        "negativeNonempty": 0,
        "positive": 10,
        "negative": 3
      },
      "body_raw": {
        "hit1": 5,
        "hit3": 6,
        "negativeNonempty": 1,
        "positive": 10,
        "negative": 3
      },
      "body_expanded": {
        "hit1": 9,
        "hit3": 9,
        "negativeNonempty": 1,
        "positive": 10,
        "negative": 3
      }
    }
  },
  "docs": [
    {
      "path": "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
      "blob": "9e95d1e9f4a3486bb5c924968d9a1f7c868272c6",
      "size": 4366,
      "linkedMethods": [
        "voi_point@1.0.0",
        "voi_oracle_bounds@1.0.0"
      ],
      "length": 1047
    },
    {
      "path": "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md",
      "blob": "9e9f769b8f8fd750ffe2e154ce1a26ae41b768a7",
      "size": 3871,
      "linkedMethods": [],
      "length": 478
    },
    {
      "path": "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md",
      "blob": "7d40f54459a7e086e9bf73f2c4906c71cebf9f7a",
      "size": 4753,
      "linkedMethods": [],
      "length": 609
    },
    {
      "path": "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md",
      "blob": "563c0dd92d7a09578e420507a12802c1f839767c",
      "size": 5707,
      "linkedMethods": [],
      "length": 1240
    },
    {
      "path": "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md",
      "blob": "a8f41752e9f4ce5200031ba5bde2c50aafdc5152",
      "size": 6140,
      "linkedMethods": [],
      "length": 1328
    },
    {
      "path": "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
      "blob": "d3c188a0ca9ca166b111d0719f03ad080473d636",
      "size": 7419,
      "linkedMethods": [],
      "length": 1578
    },
    {
      "path": "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md",
      "blob": "c862a4704d45aa379ef1187ed750aa3c88f628d1",
      "size": 5981,
      "linkedMethods": [],
      "length": 1257
    },
    {
      "path": "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md",
      "blob": "d208a80a64dca44313c4dee6e0e3fdc667b1d2c6",
      "size": 4541,
      "linkedMethods": [],
      "length": 1078
    }
  ],
  "queries": [
    [
      "Q01",
      "调查的价值为什么不同算法算出来不一样",
      "information value metric boundary",
      0
    ],
    [
      "Q02",
      "以前花了很多钱，现在还要继续吗",
      "sunk cost conversational",
      2
    ],
    [
      "Q03",
      "预期后悔和最坏后悔的计算一样吗",
      "anticipated regret minimax boundary",
      6
    ],
    [
      "Q04",
      "预计完成时间时，过去同类项目能提供什么依据",
      "planning time base rate",
      8
    ],
    [
      "Q05",
      "我用的量表到底有没有测到想测的东西",
      "construct validity measurement",
      9
    ],
    [
      "Q06",
      "有人不再回答问卷，长期结果会不会有偏差",
      "MNAR selection longitudinal bounds",
      11
    ],
    [
      "Q07",
      "只在我一个人身上尝试不同干预怎样比较",
      "sequential causal n of 1 interactions",
      14
    ],
    [
      "Q08",
      "预测概率应该如何根据真实反馈评分",
      "proper scoring feedback",
      37
    ],
    [
      "Q09",
      "只算了几个最坏后悔，差一点怎么证明排序",
      "regret precision threshold",
      -1
    ],
    [
      "Q10",
      "等调查结果的耗时不确定，会错过最后期限吗",
      "random completion time deadline",
      -2
    ],
    [
      "N01",
      "请给我写一首月亮的诗",
      "poetry moon",
      null
    ],
    [
      "N02",
      "怎么调整手机壁纸",
      "phone wallpaper",
      null
    ],
    [
      "N03",
      "帮我把图片裁剪一下",
      "crop image",
      null
    ]
  ],
  "results": [
    {
      "id": "Q01",
      "expected": [
        "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md",
          "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md"
        ],
        "body_raw": [
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md",
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md"
        ],
        "body_expanded": [
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md",
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md"
        ]
      }
    },
    {
      "id": "Q02",
      "expected": [
        "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md"
        ],
        "body_raw": [
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md",
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md"
        ],
        "body_expanded": [
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md",
          "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md",
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md"
        ]
      }
    },
    {
      "id": "Q03",
      "expected": [
        "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md",
          "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
          "research/decision_methods/VOI_RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND_2026-11-21.md"
        ],
        "body_raw": [
          "research/decision_methods/VOI_RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND_2026-11-21.md",
          "research/decision_methods/VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md",
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md"
        ],
        "body_expanded": [
          "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md",
          "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
          "research/decision_methods/VOI_RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND_2026-11-21.md"
        ]
      }
    },
    {
      "id": "Q04",
      "expected": [
        "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md",
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
        ],
        "body_raw": [
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md",
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
        ],
        "body_expanded": [
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md",
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
        ]
      }
    },
    {
      "id": "Q05",
      "expected": [
        "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md"
        ],
        "body_raw": [
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PLANNING_TIME_BASE_RATE_BOUNDARY_2026-11-23.md",
          "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md"
        ],
        "body_expanded": [
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md",
          "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md"
        ]
      }
    },
    {
      "id": "Q06",
      "expected": [
        "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md"
        ],
        "body_raw": [
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md",
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
        ],
        "body_expanded": [
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
        ]
      }
    },
    {
      "id": "Q07",
      "expected": [
        "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
        ],
        "body_raw": [
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/C001_CONSTRUCT_VALIDITY_2026-10-24.md"
        ],
        "body_expanded": [
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/ARKES_BLUMER_1985_SUNK_COST_CONVERSATIONAL_BOUNDARY_2026-11-22.md"
        ]
      }
    },
    {
      "id": "Q08",
      "expected": [
        "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md"
        ],
        "body_raw": [
          "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md",
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
        ],
        "body_expanded": [
          "research/decision_methods/C023_GNEITING_RAFTERY_2007_PROPER_SCORING_FEEDBACK_BOUNDARIES_2026-11-19.md",
          "research/decision_methods/C003_MNAR_SELECTION_LONGITUDINAL_BOUNDS_2026-10-26.md",
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
        ]
      }
    },
    {
      "id": "Q09",
      "expected": [
        "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
          "research/decision_methods/BELL_1982_ANTICIPATED_REGRET_VS_MINIMAX_BOUNDARY_2026-11-23.md"
        ],
        "body_raw": [
          "research/decision_methods/VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/VOI_RANDOMIZED_SIGNAL_POLICY_MINIMAX_BOUND_2026-11-21.md"
        ],
        "body_expanded": [
          "research/decision_methods/C031_REGRET_PRECISION_THRESHOLD_SYNTHETIC_2026-11-20.md",
          "research/decision_methods/VOI_FOUR_SIGNAL_POLICIES_MAXIMIN_CERTIFICATE_2026-11-21.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md"
        ]
      }
    },
    {
      "id": "Q10",
      "expected": [
        "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
        "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
      ],
      "ranks": {
        "filename_expanded": [
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md",
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md"
        ],
        "body_raw": [
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/ABBAS_HAZEN_2024_INFORMATION_VALUE_METRIC_BOUNDARY_2026-11-20.md",
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md"
        ],
        "body_expanded": [
          "research/decision_methods/VOI_COMPLETION_TIME_STATE_DEPENDENCE_DEADLINE_2026-11-21.md",
          "research/decision_methods/VOI_RANDOM_COMPLETION_TIME_DEADLINE_2026-11-21.md",
          "research/decision_methods/BUEHLER_GRIFFIN_ROSS_1994_PERSONAL_COMPLETION_TIME_FORECAST_BOUNDARY_2026-11-21.md"
        ]
      }
    },
    {
      "id": "N01",
      "expected": [],
      "ranks": {
        "filename_expanded": [],
        "body_raw": [],
        "body_expanded": []
      }
    },
    {
      "id": "N02",
      "expected": [],
      "ranks": {
        "filename_expanded": [],
        "body_raw": [
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
        ],
        "body_expanded": [
          "research/decision_methods/C005_SEQUENTIAL_CAUSAL_N_OF_1_INTERACTIONS_2026-10-28.md"
        ]
      }
    },
    {
      "id": "N03",
      "expected": [],
      "ranks": {
        "filename_expanded": [],
        "body_raw": [],
        "body_expanded": []
      }
    }
  ]
}
```
## 复算
Node >=18；从第29轮固定config/postings与本轮8份文件路径加载原始字节，使用Node crypto SHA1验证每份后再按下方index/rank运行；本轮实际连接器采用下方原创SHA1及base64/UTF8，不依赖Node API。完整154份的既有build_index.js仍可在完整工作树使用。
```js
function utf8(s){let a=[];for(const x of s){let c=x.codePointAt(0);if(c<128)a.push(c);else if(c<2048)a.push(192|(c>>6),128|(c&63));else if(c<65536)a.push(224|(c>>12),128|((c>>6)&63),128|(c&63));else a.push(240|(c>>18),128|((c>>12)&63),128|((c>>6)&63),128|(c&63));}return a}
function b64(s){const alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/",out=[];let v=0,n=0;for(const c of s){if(/\s/.test(c))continue;if(c==="=")break;const x=alphabet.indexOf(c);if(x<0)throw Error("invalid base64");v=(v<<6)|x;n+=6;if(n>=8){n-=8;out.push((v>>n)&255)}}return out}
function decode(a){let s="";for(let i=0;i<a.length;){let b=a[i++],c=b;if(b>=240)c=((b&7)<<18)|((a[i++]&63)<<12)|((a[i++]&63)<<6)|(a[i++]&63);else if(b>=224)c=((b&15)<<12)|((a[i++]&63)<<6)|(a[i++]&63);else if(b>=192)c=((b&31)<<6)|(a[i++]&63);s+=String.fromCodePoint(c)}return s}
function sha1(input){const a=input.slice(),bits=a.length*8;a.push(128);while(a.length%64!==56)a.push(0);for(let i=7;i>=0;i--)a.push(Math.floor(bits/2**(8*i))&255);let h=[0x67452301,0xefcdab89,0x98badcfe,0x10325476,0xc3d2e1f0];const rot=(x,n)=>(x<<n)|(x>>>(32-n));for(let p=0;p<a.length;p+=64){let w=[];for(let i=0;i<16;i++){let k=p+4*i;w.push((a[k]<<24)|(a[k+1]<<16)|(a[k+2]<<8)|a[k+3])}for(let i=16;i<80;i++)w.push(rot(w[i-3]^w[i-8]^w[i-14]^w[i-16],1));let [x,y,z,u,v]=h;for(let i=0;i<80;i++){const f=i<20?(y&z)|(~y&u):i<40?y^z^u:i<60?(y&z)|(y&u)|(z&u):y^z^u,k=i<20?0x5a827999:i<40?0x6ed9eba1:i<60?0x8f1bbcdc:0xca62c1d6,t=(rot(x,5)+f+v+k+w[i])|0;v=u;u=z;z=rot(y,30);y=x;x=t}h=h.map((n,i)=>(n+[x,y,z,u,v][i])|0)}return h.map(x=>(x>>>0).toString(16).padStart(8,"0")).join("")}
function tokens(s){let out=[];for(const m of s.toLowerCase().matchAll(/[a-z]+[0-9]*|[\u3400-\u9fff]+/g)){let v=m[0];if(/^[a-z]/.test(v)){if(v.length>1)out.push(v)}else for(let i=0;i<v.length-1;i++)out.push(v.slice(i,i+2))}return out}
function index(d,s){const ts=tokens(s),m=new Map();for(const t of ts)m.set(t,(m.get(t)||0)+1);return {...d,length:ts.length,terms:[...m.entries()].sort((a,b)=>a[0]<b[0]?-1:a[0]>b[0]?1:0)}}
function rank(ds,query,field){const ts=[...new Set(tokens(query))],vs=ds.map(d=>field==="filename"?index(d,d.path.split("/").at(-1)):d),av=vs.reduce((s,v)=>s+v.length,0)/vs.length,maps=vs.map(v=>new Map(v.terms)),df=ts.map(t=>maps.filter(m=>m.has(t)).length);return vs.map((v,i)=>({path:v.path,score:ts.reduce((s,t,j)=>{let n=maps[i].get(t)||0;return s+(n?Math.log(1+(vs.length-df[j]+.5)/(df[j]+.5))*n*2.2/(n+1.2*(.25+.75*v.length/av)):0)},0)})).filter(x=>x.score>0).sort((a,b)=>b.score-a.score||a.path.localeCompare(b.path))}
const queries=[["Q01","调查的价值为什么不同算法算出来不一样","information value metric boundary",0],["Q02","以前花了很多钱，现在还要继续吗","sunk cost conversational",2],["Q03","预期后悔和最坏后悔的计算一样吗","anticipated regret minimax boundary",6],["Q04","预计完成时间时，过去同类项目能提供什么依据","planning time base rate",8],["Q05","我用的量表到底有没有测到想测的东西","construct validity measurement",9],["Q06","有人不再回答问卷，长期结果会不会有偏差","MNAR selection longitudinal bounds",11],["Q07","只在我一个人身上尝试不同干预怎样比较","sequential causal n of 1 interactions",14],["Q08","预测概率应该如何根据真实反馈评分","proper scoring feedback",37],["Q09","只算了几个最坏后悔，差一点怎么证明排序","regret precision threshold",-1],["Q10","等调查结果的耗时不确定，会错过最后期限吗","random completion time deadline",-2],["N01","请给我写一首月亮的诗","poetry moon",null],["N02","怎么调整手机壁纸","phone wallpaper",null],["N03","帮我把图片裁剪一下","crop image",null]];
const ids=[0,2,6,8,9,11,14,37];
const fs=require('node:fs'),path=require('node:path');
const root=process.argv[2];if(!root)throw Error('repo root required');
const p="research/decision_hub/2026-11-24-native-method-contract-index/";
const cfg=JSON.parse(fs.readFileSync(path.join(root,p+'config.json'),'utf8'));
const old=JSON.parse(fs.readFileSync(path.join(root,p+'postings_sample.json'),'utf8'));
const docs=ids.map(i=>{const d=cfg.assets[i],b=[...fs.readFileSync(path.join(root,d.path))];if(b.length!==d.size||sha1([...utf8('blob '+b.length+'\0'),...b])!==d.blob)throw Error('identity');return index(d,decode(b));});
for(const q of queries)console.log(q[0],['filename_expanded','body_raw','body_expanded'].map(m=>rank([...old,...docs],m==='body_raw'?q[1]:m==='filename_expanded'?q[2]:q[1]+' '+q[2],m==='filename_expanded'?'filename':'body').slice(0,3)));
```
## 边界与后续
全库仍受本地DNS及单次连接器调用数量限制；本轮保留真实增量，不冒充完成全部154份。优先在有实际仓库的零费用授权环境运行原有全库构建器及完整原生registry.describe/validate，再开展冻结独立查询、目标与否定、多意图、来源变化及权限测试。没有重新审查R项、真实Mac/Qwen、手机、用户或科学独立验收；无生产修改、Codex、CI、训练、合并、部署、冻结协议变更或新增费用。B04/B06/B08/B11候选增量。

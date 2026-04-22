import { defineConfig } from 'vitepress'
import { withMermaid } from 'vitepress-plugin-mermaid'

export default withMermaid(defineConfig({
  lang: 'zh-CN',
  title: '倪海厦讲中医',
  description: '中医学习平台',
  lastUpdated: true,
  cleanUrls: true,
  appearance: 'dark',
  
  head: [
    ['link', { rel: 'icon', href: '/logo.svg' }]
  ],

  markdown: {
    math: true
  },
  
  themeConfig: {
    logo: '/logo.svg',
    nav: [
      { text: '首页', link: '/' },
      { text: '指南', link: '/guide/' },
      { text: '针灸大成', link: '/acupuncture/' },
      { text: '黄帝内经', link: '/huangdi/' },
      { text: '神农本草经', link: '/shennong/' },
      { text: '伤寒论', link: '/shanghan/' },
      { text: '金匮要略', link: '/jinkui/' }
    ],

    sidebar: {
      '/guide/': [
        {
          text: '指南',
          items: [
            { text: '介绍', link: '/guide/' },
            { text: '快速开始', link: '/guide/getting-started' }
          ]
        }
      ],
      '/acupuncture/': [
        {
          text: '针灸大成',
          items: [
            { text: '概述', link: '/acupuncture/' },
            {
              text: '十二正经',
              collapsed: false,
              items: [
                { text: '肺经', link: '/acupuncture/meridians/lung/' },
                { text: '大肠经', link: '/acupuncture/meridians/large_intestine/' },
                { text: '胃经', link: '/acupuncture/meridians/stomach/' },
                { text: '脾经', link: '/acupuncture/meridians/spleen/' },
                { text: '心经', link: '/acupuncture/meridians/heart/' },
                { text: '小肠经', link: '/acupuncture/meridians/small_intestine/' },
                { text: '膀胱经', link: '/acupuncture/meridians/bladder/' },
                { text: '肾经', link: '/acupuncture/meridians/kidney/' },
                { text: '心包经', link: '/acupuncture/meridians/pericardium/' },
                { text: '三焦经', link: '/acupuncture/meridians/triple_energizer/' },
                { text: '胆经', link: '/acupuncture/meridians/gallbladder/' },
                { text: '肝经', link: '/acupuncture/meridians/liver/' },
                { text: '十二经总结', link: '/acupuncture/meridians/12Summarize/' }
                
              ]
            },
            {
              text: '奇经八脉',
              collapsed: false,
              items: [
                { text: '任脉', link: '/acupuncture/extraordinary/ren/' },
                { text: '督脉', link: '/acupuncture/extraordinary/du/' },
                { text: '奇经八脉合集', link: '/acupuncture/extraordinary/compilation/' }
              ]
            },
            {
              text: '针法',
              collapsed: false,
              items: [
                { text: '针法', link: '/acupuncture/needling/' }
              ]
            },
            {
              text: '灸法',
              collapsed: false,
              items: [
                { text: '隔姜灸', link: '/acupuncture/moxibustion/ginger/' },
                { text: '隔蒜灸', link: '/acupuncture/moxibustion/garlic/' }
              ]
            }
          ]
        }
      ],
      '/huangdi/': [
        {
          text: '黄帝内经',
          items: [
            { text: '概述', link: '/huangdi/' },
            {
              text: '系统总体设计',
              collapsed: false,
              items: [
                { text: '系统自检', link: '/huangdi/summary/' },
                { text: '阴阳', link: '/huangdi/summary/' },
                { text: '寒热', link: '/huangdi/summary/' },
                { text: '表里虚实', link: '/huangdi/summary/' },
                { text: '五大子系统', link: '/huangdi/summary/' }
              ]
            },
            {
              text: '子系统设计',
              collapsed: false,
              items: [
                { text: '肝', link: '/huangdi/subdesign/' },
                { text: '心', link: '/huangdi/subdesign/' },
                { text: '脾', link: '/huangdi/subdesign/' },
                { text: '肺', link: '/huangdi/subdesign/' },
                { text: '肾', link: '/huangdi/subdesign/' }
              ]
            },
            {
              text: '网络结构设计',
              collapsed: false,
              items: [
                { text: '主干线设计', link: '/huangdi/networkdesign/' },
                { text: '特定穴位-水热穴等', link: '/huangdi/networkdesign/' }
              ]
            },
            {
              text: '常见问题集合',
              collapsed: false,
              items: [
                { text: '热', link: '/huangdi/case/' },
                { text: '痛', link: '/huangdi/case/' },
                { text: '腹中论', link: '/huangdi/case/' },
                { text: '络病', link: '/huangdi/case/' }
              ]
            },
            {
              text: '针刺',
              collapsed: false,
              items: [
                { text: '补泻法', link: '/huangdi/rules/' },
                { text: '针刺法则', link: '/huangdi/rules/' }
              ]
            },
            {
              text: '脉法',
              collapsed: false,
              items: [
                { text: '脉法基础', link: '/huangdi/pulse/' }
              ]
            },
            {
              text: '其它',
              collapsed: false,
              items: [
                { text: '其它', link: '/huangdi/others/' }
              ]
            },
            {
              text: '附录',
              collapsed: false,
              items: [
                { text: '人体故障诊断算法', link: '/huangdi/appendix/failure.md' },
                { text: '故障排除的调试方法', link: '/huangdi/appendix/debug.md' },
                { text: '对称映射能量衰减理论', link: '/huangdi/appendix/symmetryTheory.md' },
                { text: '总线协议代号表', link: '/huangdi/appendix/lineProtocol.md' },
                { text: '人体系统手册总纲', link: '/huangdi/appendix/outline.md' }
              ]
            }
          ]
        }
      ],
      '/shennong/': [
        {
          text: '神农本草经',
          items: [
            { text: '概述', link: '/shennong/' },
            { text: '上经', link: '/shennong/upper/' },
            { text: '中经', link: '/shennong/middle/' },
            { text: '下经', link: '/shennong/lower/' },
            { text: '增补', link: '/shennong/supplement/' }
          ]
        }
      ],
      '/shanghan/': [
        {
          text: '伤寒论',
          items: [
            { text: '概述', link: '/shanghan/' }
          ]
        }
      ],
      '/jinkui/': [
        {
          text: '金匮要略',
          items: [
            { text: '概述', link: '/jinkui/' }
          ]
        }
      ]
    },

    socialLinks: [
      { icon: 'github', link: 'https://github.com' }
    ],

    footer: {
      message: '倪海厦讲中医 - 中医学习平台',
      copyright: 'Copyright © 2023-present'
    },

    search: {
      provider: 'local'
    }
  }
}))
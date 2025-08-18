import { defineConfig } from 'vitepress'

export default defineConfig({
  lang: 'zh-CN',
  title: '倪海厦讲中医',
  description: '中医学习平台',
  lastUpdated: true,
  cleanUrls: true,
  appearance: 'dark',
  
  head: [
    ['link', { rel: 'icon', href: '/logo.svg' }]
  ],

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
                { text: '肝经', link: '/acupuncture/meridians/liver/' }
              ]
            },
            {
              text: '奇经八脉',
              collapsed: false,
              items: [
                { text: '任脉', link: '/acupuncture/extraordinary/ren/' },
                { text: '督脉', link: '/acupuncture/extraordinary/du/' },
                { text: '冲脉', link: '/acupuncture/extraordinary/chong/' },
                { text: '带脉', link: '/acupuncture/extraordinary/dai/' },
                { text: '阴维脉', link: '/acupuncture/extraordinary/yinwei/' },
                { text: '阳维脉', link: '/acupuncture/extraordinary/yangwei/' },
                { text: '阴跷脉', link: '/acupuncture/extraordinary/yinqiao/' },
                { text: '阳跷脉', link: '/acupuncture/extraordinary/yangqiao/' }
              ]
            },
            {
              text: '针法',
              collapsed: false,
              items: [
                { text: '烧山火', link: '/acupuncture/needling/burning_mountain/' },
                { text: '透心凉', link: '/acupuncture/needling/penetrating_cold/' }
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
            { text: '素问', link: '/huangdi/suwen/' },
            { text: '灵枢', link: '/huangdi/lingshu/' }
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
})
# =========================================================
# app.py
# مساعد لائحة الحوافز والمكافآت - جامعة البطانة
# =========================================================

import os
import gradio as gr

# =========================================================
# استيراد ملف الدوال بالكامل
# =========================================================

import system_functions as sf


# =========================================================
# مسار صورة الشعار
# =========================================================

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

LOGO_PATH = os.path.join(
    BASE_DIR,
    "logo.png"
)


# =========================================================
# CSS - تصميم النظام
# =========================================================

custom_css = """
/* =====================================================
   الصفحة الرئيسية
   ===================================================== */

body {
    direction: rtl;
}

/* خلفية النظام */
.main-container {
    position: relative;
    background-color: rgba(255, 255, 255, 0.94);

    background-image:
        linear-gradient(
            rgba(255,255,255,0.91),
            rgba(255,255,255,0.91)
        ),
        url("/file=logo.png");

    background-position: center;
    background-repeat: no-repeat;
    background-size: 500px;
    background-attachment: fixed;

    min-height: 100vh;
}

/* العنوان */
.system-title {
    text-align: center;
    font-size: 30px !important;
    font-weight: bold;
    margin-bottom: 5px;
}

/* العنوان الفرعي */
.system-subtitle {
    text-align: center;
    font-size: 18px !important;
    margin-bottom: 20px;
}

/* البطاقات */
.dashboard-card {
    border-radius: 15px !important;
    padding: 15px !important;
}

/* الأزرار */
button {
    border-radius: 10px !important;
}

/* منطقة تسجيل الدخول */
.login-box {
    max-width: 500px;
    margin: auto;
    padding: 25px;
}

/* العنوان */
.login-title {
    text-align: center;
    font-size: 28px !important;
    font-weight: bold;
}

/* رسالة الخطأ */
.error-message {
    text-align: center;
    font-weight: bold;
}

/* إخفاء بعض العناصر غير المهمة */
footer {
    display: none !important;
}
"""


# =========================================================
# إنشاء الواجهة
# =========================================================

with gr.Blocks(
    title="مساعد لائحة الحوافز والمكافآت - جامعة البطانة",
    css=custom_css
) as demo:

    # =====================================================
    # شاشة تسجيل الدخول
    # =====================================================

    login_screen = gr.Column(
        visible=True,
        elem_classes="login-box"
    )

    with login_screen:

        gr.Markdown(
            """
# 🏛 مساعد لائحة الحوافز والمكافآت

## جامعة البطانة

### 🔐 تسجيل الدخول
""",
            elem_classes="login-title"
        )

        username = gr.Textbox(
            label="👤 اسم المستخدم",
            placeholder="أدخل اسم المستخدم",
            
        )

        password = gr.Textbox(
            label="🔑 رمز الدخول",
            placeholder="أدخل رمز الدخول",
            type="password",
            
        )

        login_button = gr.Button(
            "🔓 تسجيل الدخول",
            variant="primary"
        )

        login_message = gr.Markdown(
            ""
        )


    # =====================================================
    # النظام الرئيسي
    # =====================================================

    main_screen = gr.Column(
        visible=False,
        elem_classes="main-container"
    )

    with main_screen:

        # =================================================
        # رأس النظام
        # =================================================

        gr.Markdown(
            """
# 🏛 مساعد لائحة الحوافز والمكافآت

## جامعة البطانة

### 📚 نظام إلكتروني للبحث والاستعلام عن الحوافز والمكافآت
""",
            elem_classes="system-title"
        )

        welcome_message = gr.Markdown(
            ""
        )
        # =================================================
        # لوحة التحكم
        # =================================================

        gr.Markdown(
            """
# 🎛️ لوحة التحكم
"""
        )

        with gr.Row():

            search_button = gr.Button(
                "🔎 البحث",
                variant="primary"
            )

            entitlement_button = gr.Button(
                "🧮 حساب الاستحقاق"
            )

            calculator_button = gr.Button(
                "🧮 الآلة الحاسبة"
            )

            statistics_button = gr.Button(
                "📊 الإحصائيات"
            )


        with gr.Row():

            global_button = gr.Button(
                "🌐 البحث الشامل"
            )

            system_button = gr.Button(
                "ℹ️ معلومات النظام"
            )

            logout_button = gr.Button(
                "🚪 تسجيل الخروج",
                variant="stop"
            )


        # =================================================
        # تبويبات النظام
        # =================================================

        with gr.Tabs():

            # =================================================
            # 1 - البحث
            # =================================================

            with gr.Tab(
                "🔎 البحث عن المكافآت",
                id=0
            ) as search_tab:

                gr.Markdown(
                    """
## 🔎 البحث عن وظيفة أو مكافأة

اكتب اسم الوظيفة مثل:

المدير

أو:

الوكيل

أو:

عميد الكلية
"""
                )

                search_input = gr.Textbox(
                    label="اسم الوظيفة",
                    placeholder="اكتب اسم الوظيفة هنا...",
                )

                reward_dropdown = gr.Dropdown(
                    choices=sf.get_reward_types(),
                    value="الكل",
                    label="🎁 نوع المكافأة",
                )

                with gr.Row():

                    search_execute = gr.Button(
                        "🔎 تنفيذ البحث",
                        variant="primary"
                    )

                    search_clear = gr.Button(
                        "🗑 مسح"
                    )

                search_result = gr.Dataframe(
                    headers=None,
                    interactive=False,
                    wrap=True
                )


            # =================================================
            # 2 - حساب الاستحقاق
            # =================================================

            with gr.Tab(
                "🧮 حساب الاستحقاق",
                id=1
            ) as entitlement_tab:

                gr.Markdown(
                    """
## 🧮 حساب استحقاق الوظيفة

أدخل الوظيفة والعدد المطلوب حسابه.

> لا توجد خاصية جمع وظيفتين؛ الحساب يتم للوظيفة المحددة فقط.
"""
                )

                entitlement_job = gr.Textbox(
                    label="👤 المسمى الوظيفي",
                    placeholder="مثال: المدير",
    
                )

                entitlement_reward = gr.Dropdown(
                    choices=sf.get_reward_types(),
                    value="الكل",
                    label="🎁 نوع المكافأة",
                    
                    
                )

                entitlement_quantity = gr.Number(
                    label="🔢 العدد",
                    value=1,
                    minimum=1,
                    precision=0
                )

                entitlement_execute = gr.Button(
                    "🧮 حساب الاستحقاق",
                    variant="primary"
                )

                entitlement_result = gr.Markdown(
                    ""
                )


            # =================================================
            # 3 - الآلة الحاسبة
            # =================================================

            with gr.Tab(
                "🧮 الآلة الحاسبة",
                id=2
            ) as calculator_tab:
                gr.Markdown(
                    """
# 🧮 الآلة الحاسبة

استخدم هذه الآلة لإجراء العمليات الحسابية.

### أمثلة:

420000 + 350000

70000 * 5

500000 - 75000

70000 / 2

(50000 + 30000) * 2

يمكنك أيضًا استخدام:

× بدل *

و:

÷ بدل /
"""
                )

                calculator_input = gr.Textbox(
                    label="✏️ العملية الحسابية",
                    placeholder="اكتب العملية هنا...",
                    rtl=False
                )

                with gr.Row():

                    calculator_execute = gr.Button(
                        "🧮 احسب",
                        variant="primary"
                    )

                    calculator_clear = gr.Button(
                        "🗑 مسح"
                    )

                calculator_result = gr.Markdown(
                    ""
                )


            # =================================================
            # 4 - الإحصائيات
            # =================================================

            with gr.Tab(
                "📊 الإحصائيات",
                id=3
            ) as statistics_tab:

                gr.Markdown(
                    """
# 📊 إحصائيات النظام

تعرض هذه الصفحة معلومات مختصرة عن البيانات الموجودة في النظام.
"""
                )

                statistics_button_2 = gr.Button(
                    "🔄 تحديث الإحصائيات",
                    variant="primary"
                )

                statistics_result = gr.Markdown(
                    ""
                )

                statistics_table = gr.Dataframe(
                    interactive=False
                )


            # =================================================
            # 5 - البحث الشامل
            # =================================================

            with gr.Tab(
                "🌐 البحث الشامل",
                id=4
            ) as global_tab:

                gr.Markdown(
                    """
# 🌐 البحث الشامل

ابحث عن كلمة أو عبارة في جميع حقول البيانات.
"""
                )

                global_input = gr.Textbox(
                    label="🔎 البحث",
                    placeholder="اكتب كلمة للبحث في جميع البيانات...",
                
                )

                with gr.Row():

                    global_execute = gr.Button(
                        "🌐 تنفيذ البحث",
                        variant="primary"
                    )

                    global_clear = gr.Button(
                        "🗑 مسح"
                    )

                global_result = gr.Dataframe(
                    interactive=False,
                    wrap=True
                )


            # =================================================
            # 6 - معلومات النظام
            # =================================================

            with gr.Tab(
                "ℹ️ معلومات النظام",
                id=5
            ) as system_tab:

                system_result = gr.Markdown(
                    sf.system_info()
                )


            # =================================================
            # 7 - البيانات
            # =================================================

            with gr.Tab(
                "📋 جميع البيانات",
                id=6
            ) as all_data_tab:

                gr.Markdown(
                    """
# 📋 جميع بيانات اللائحة
"""
                )

                refresh_data_button = gr.Button(
                    "🔄 تحديث البيانات"
                )

                all_data_result = gr.Dataframe(
                    value=sf.get_all_data(),
                    interactive=False,
                    wrap=True
                )

                with gr.Row():

                    export_csv_button = gr.Button(
                        "📥 تصدير CSV"
                    )

                    export_excel_button = gr.Button(
                        "📊 تصدير Excel"
                    )
                    csv_file = gr.File(
                    label="ملف CSV",
                    visible=False
                )

                excel_file = gr.File(
                    label="ملف Excel",
                    visible=False
                )


        # =================================================
        # رسالة أسفل النظام
        # =================================================

        gr.Markdown(
            """
---

### 🏛 جامعة البطانة
مساعد لائحة الحوافز والمكافآت - تعديل 2025م

📌 النظام مخصص للبحث والاستعلام والحساب والإحصائيات.
"""
        )


    # =====================================================
    # أحداث تسجيل الدخول
    # =====================================================

    login_button.click(
        fn=sf.login,
        inputs=[
            username,
            password
        ],
        outputs=[
            login_screen,
            main_screen,
            welcome_message,
            login_message
        ]
    )


    # =====================================================
    # تسجيل الخروج
    # =====================================================

    logout_button.click(
        fn=sf.logout,
        inputs=[],
        outputs=[
            login_screen,
            main_screen,
            welcome_message,
            login_message
        ]
    )


    # =====================================================
    # البحث
    # =====================================================

    search_execute.click(
        fn=sf.search_by_job_and_reward,
        inputs=[
            search_input,
            reward_dropdown
        ],
        outputs=[
            search_result
        ]
    )


    # البحث عند الضغط على Enter
    search_input.submit(
        fn=sf.search_by_job_and_reward,
        inputs=[
            search_input,
            reward_dropdown
        ],
        outputs=[
            search_result
        ]
    )


    # =====================================================
    # مسح البحث
    # =====================================================

    search_clear.click(
        fn=lambda: ("", "الكل", None),
        inputs=[],
        outputs=[
            search_input,
            reward_dropdown,
            search_result
        ]
    )


    # =====================================================
    # حساب الاستحقاق
    # =====================================================

    entitlement_execute.click(
        fn=sf.calculate_entitlement,
        inputs=[
            entitlement_job,
            entitlement_reward,
            entitlement_quantity
        ],
        outputs=[
            entitlement_result
        ]
    )


    # =====================================================
    # الآلة الحاسبة
    # =====================================================

    calculator_execute.click(
        fn=sf.calculator,
        inputs=[
            calculator_input
        ],
        outputs=[
            calculator_result
        ]
    )


    calculator_input.submit(
        fn=sf.calculator,
        inputs=[
            calculator_input
        ],
        outputs=[
            calculator_result
        ]
    )


    calculator_clear.click(
        fn=lambda: ("", ""),
        inputs=[],
        outputs=[
            calculator_input,
            calculator_result
        ]
    )


    # =====================================================
    # الإحصائيات
    # =====================================================

    statistics_button.click(
        fn=sf.get_statistics,
        inputs=[],
        outputs=[
            statistics_result
        ]
    )


    statistics_button_2.click(
        fn=sf.get_statistics,
        inputs=[],
        outputs=[
            statistics_result
        ]
    )


    # جدول الإحصائيات
    statistics_button_2.click(
        fn=sf.get_statistics_dataframe,
        inputs=[],
        outputs=[
            statistics_table
        ]
    )


    # =====================================================
    # البحث الشامل
    # =====================================================
    global_execute.click(
        fn=sf.global_search,
        inputs=[
            global_input
        ],
        outputs=[
            global_result
        ]
    )


    global_input.submit(
        fn=sf.global_search,
        inputs=[
            global_input
        ],
        outputs=[
            global_result
        ]
    )


    global_clear.click(
        fn=lambda: ("", None),
        inputs=[],
        outputs=[
            global_input,
            global_result
        ]
    )


    # =====================================================
    # تحديث جميع البيانات
    # =====================================================

    refresh_data_button.click(
        fn=sf.get_all_data,
        inputs=[],
        outputs=[
            all_data_result
        ]
    )


    # =====================================================
    # تصدير CSV
    # =====================================================

    export_csv_button.click(
        fn=sf.export_csv,
        inputs=[],
        outputs=[
            csv_file
        ]
    )

    export_csv_button.click(
        fn=lambda: gr.update(visible=True),
        inputs=[],
        outputs=[
            csv_file
        ]
    )


    # =====================================================
    # تصدير Excel
    # =====================================================

    export_excel_button.click(
        fn=sf.export_excel,
        inputs=[],
        outputs=[
            excel_file
        ]
    )

    export_excel_button.click(
        fn=lambda: gr.update(visible=True),
        inputs=[],
        outputs=[
            excel_file
        ]
    )


    # =====================================================
    # أزرار لوحة التحكم
    # =====================================================

    search_button.click(
        fn=lambda: None,
        inputs=[],
        outputs=[]
    )

    entitlement_button.click(
        fn=lambda: None,
        inputs=[],
        outputs=[]
    )

    calculator_button.click(
        fn=lambda: None,
        inputs=[],
        outputs=[]
    )

    statistics_button.click(
        fn=sf.get_statistics,
        inputs=[],
        outputs=[
            statistics_result
        ]
    )

    global_button.click(
        fn=lambda: None,
        inputs=[],
        outputs=[]
    )

    system_button.click(
        fn=sf.system_info,
        inputs=[],
        outputs=[
            system_result
        ]
    )


# =========================================================
# تشغيل البرنامج
# =========================================================

if __name__ == "__main__":

    demo.launch(
        server_name="127.0.0.1",
        server_port=7860,
        inbrowser=True,
        share=False
    )
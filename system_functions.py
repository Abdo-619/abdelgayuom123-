# =========================================================
# system_functions.py
# دوال نظام مساعد لائحة الحوافز والمكافآت
# جامعة البطانة
# =========================================================

import os
import re
import ast
import operator
import tempfile
import unicodedata
from datetime import datetime

import pandas as pd
import gradio as gr

from data import df


# =========================================================
# بيانات تسجيل الدخول
# =========================================================

USERNAME = "admin"
PASSWORD = "1234"


# =========================================================
# توحيد النص العربي
# =========================================================

def normalize_text(text):

    if text is None:
        return ""

    text = str(text).strip().lower()

    # إزالة التشكيل
    text = "".join(
        char
        for char in unicodedata.normalize(
            "NFD",
            text
        )
        if unicodedata.category(char) != "Mn"
    )

    # توحيد بعض الحروف العربية
    replacements = {
        "أ": "ا",
        "إ": "ا",
        "آ": "ا",
        "ٱ": "ا",
        "ى": "ي",
        "ة": "ه",
        "ؤ": "و",
        "ئ": "ي",
    }

    for old, new in replacements.items():
        text = text.replace(
            old,
            new
        )

    # توحيد المسافات
    text = re.sub(
        r"\s+",
        " ",
        text
    )

    return text.strip()


# =========================================================
# تجهيز عمود البحث
# =========================================================

try:

    if "وظيفة" in df.columns:

        df["وظيفة_بحث"] = (
            df["وظيفة"]
            .apply(normalize_text)
        )

except Exception:

    pass


# =========================================================
# رسالة الترحيب حسب الوقت
# =========================================================

def get_greeting():

    hour = datetime.now().hour

    if 5 <= hour < 10:

        return "🌅 صباح الخير"

    elif 10 <= hour < 17:

        return "☀️ نهارك سعيد"

    else:

        return "🌙 مساء الخير"


# =========================================================
# تسجيل الدخول
# =========================================================

def login(
    username,
    password
):

    username = (
        ""
        if username is None
        else str(username).strip()
    )

    password = (
        ""
        if password is None
        else str(password).strip()
    )

    if (
        username == USERNAME
        and password == PASSWORD
    ):

        greeting = get_greeting()

        message = f"""
# 🎉 تم تسجيل الدخول بنجاح

## {greeting}، {username} 👋

مرحباً بك في مساعد لائحة الحوافز والمكافآت - جامعة البطانة.

يمكنك الآن استخدام:

🔎 البحث عن الوظائف والمكافآت

🧮 حساب الاستحقاق

🧮 الآلة الحاسبة

📊 الإحصائيات

🌐 البحث الشامل

📥 تصدير البيانات
"""

        return (
            gr.update(
                visible=False
            ),

            gr.update(
                visible=True
            ),

            message,

            ""
        )

    return (
        gr.update(
            visible=True
        ),

        gr.update(
            visible=False
        ),

        "",

        "❌ اسم المستخدم أو رمز الدخول غير صحيح."
    )
def get_reward_types():
    # استبدل هذه القائمة بالقيم أو الخيارات التي تريد عرضها
    return ["نوع 1", "نوع 2", "نوع 3"]

# =========================================================
# تسجيل الخروج
# =========================================================

def logout():

    return (
        gr.update(
            visible=True
        ),

        gr.update(
            visible=False
        ),

        "",

        ""
    )


# =========================================================
# البحث عن الوظائف
# =========================================================

def search_jobs(
    query=""
):

    if query is None:

        query = ""

    query = str(
        query
    ).strip()

    if not query:

        return df.copy()

    normalized_query = normalize_text(
        query
    )

    try:

        search_column = (
            df["وظيفة"]
            .apply(normalize_text)
        )
        mask = search_column.str.contains(
            normalized_query,
            case=False,
            na=False,
            regex=False
        )

        return df[
            mask
        ].copy()

    except Exception:

        return pd.DataFrame()
# =========================================================
# الحصول على أنواع المكافآت
# =========================================================

def get_reward_types():
    try:
        rewards = (
            df["نوع_المكافأة"]
            .dropna()
            .astype(str)
            .drop_duplicates()
            .tolist()
        )

        rewards.sort()

        return ["الكل"] + rewards

    except Exception:
        return ["الكل"]
# =========================================================
# البحث حسب الوظيفة ونوع المكافأة
# =========================================================

def search_by_job_and_reward(
    job="",
    reward_type="الكل"
):

    result = df.copy()

    # البحث حسب الوظيفة
    if job:

        normalized_job = normalize_text(
            job
        )

        job_column = (
            result["وظيفة"]
            .apply(normalize_text)
        )

        result = result[
            job_column.str.contains(
                normalized_job,
                case=False,
                na=False,
                regex=False
            )
        ]

    # البحث حسب نوع المكافأة
    if (
        reward_type
        and reward_type != "الكل"
        and "نوع_المكافأة" in result.columns
    ):

        result = result[
            result["نوع_المكافأة"]
            .astype(str)
            == str(reward_type)
        ]

    # إزالة عمود البحث الداخلي
    if "وظيفة_بحث" in result.columns:

        result = result.drop(
            columns=[
                "وظيفة_بحث"
            ]
        )

    return result


# =========================================================
# البحث الرئيسي
# =========================================================

def respond(
    message,
    history=None
):

    if (
        message is None
        or not str(message).strip()
    ):

        return """
⚠️ يرجى كتابة اسم الوظيفة أولاً.

مثال:

- المدير
- الوكيل
- عميد الكلية
- المسجل
- العمال
"""

    message = str(
        message
    ).strip()

    results = search_jobs(
        message
    )

    if results.empty:

        return f"""
❌ لم يتم العثور على سجلات مطابقة لـ:

{message}

### 🔎 جرّب البحث باستخدام:

- المدير
- الوكيل
- أمين الشؤون العلمية
- عميد الكلية
- نائب عميد الكلية
- المسجل
- الحرس الجامعي
- العمال
"""

    response = f"""
# 🔍 نتائج البحث

### البحث عن:

{message}

| المسمى الوظيفي | نوع الاستحقاق / المكافأة | الفئة | العملة | الملاحظات |
|---|---|---:|---|---|
"""

    for _, row in results.iterrows():

        job = row.get(
            "وظيفة",
            ""
        )

        reward = row.get(
            "نوع_المكافأة",
            ""
        )

        amount = row.get(
            "الفئة_بالجنيه",
            ""
        )

        currency = row.get(
            "العملة",
            "جنيه"
        )

        note = row.get(
            "ملاحظات",
            ""
        )

        response += (
            f"| {job} | "
            f"{reward} | "
            f"{amount} | "
            f"{currency} | "
            f"{note} |\n"
        )

    response += """

---

📌 المصدر: لائحة المكافآت والحوافز لجامعة البطانة - تعديل 2025م.
"""

    return response


# =========================================================
# استخراج رقم من النص
# =========================================================

def extract_number(
    value
):

    if value is None:

        return 0.0

    if isinstance(
        value,
        (int, float)
    ):

        return float(
            value
        )

    text = str(
        value
    )

    # إزالة الفواصل
    text = text.replace(
        ",",
        ""
    )

    # تحويل الأرقام العربية
    arabic_numbers = {
        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
    }

    for old, new in arabic_numbers.items():

        text = text.replace(
            old,
            new
        )

    match = re.search(
        r"\d+(?:\.\d+)?",
        text
    )

    if match:

        try:

            return float(
                match.group()
            )

        except Exception:

            return 0.0

    return 0.0


# =========================================================
# حساب الاستحقاق
# =========================================================

def calculate_entitlement(
    job="",
    reward_type="الكل",
    quantity=1
):

    if job is None:

        job = ""

    job = str(
        job
    ).strip()

    if not job:

        return """
⚠️ يرجى إدخال المسمى الوظيفي.
"""

    try:

        quantity = float(
            quantity
        )

    except Exception:

        quantity = 1

    if quantity <= 0:

        quantity = 1

    results = search_by_job_and_reward(
        job,
        reward_type
    )

    if results.empty:

        return f"""
❌ لم يتم العثور على وظيفة:

{job}
"""

    response = f"""
# 🧮 حساب الاستحقاق

### الوظيفة:

{job}

### العدد:

{quantity:g}

---

"""

    total = 0.0

    has_numeric_value = False

    for _, row in results.iterrows():

        amount = row.get(
            "الفئة_بالجنيه",
            ""
        )

        numeric_amount = extract_number(
            amount
        )

        if numeric_amount > 0:

            calculated = (
                numeric_amount
                * quantity
            )

            total += calculated

            has_numeric_value = True

            response += (
                f"### {row.get('وظيفة', '')}\n\n"
                f"نوع المكافأة: "
                f"{row.get('نوع_المكافأة', '')}\n\n"
                f"الفئة: {amount} جنيه\n\n"
                f"الحساب: "
                f"{numeric_amount:g} × "
                f"{quantity:g} = "
                f"{calculated:,.0f} جنيه\n\n"
                f"---\n\n"
            )

        else:

            response += (
                f"### {row.get('وظيفة', '')}\n\n"
                f"نوع المكافأة: "
                f"{row.get('نوع_المكافأة', '')}\n\n"
                f"الفئة: {amount}\n\n"
                f"---\n\n"
            )

    if has_numeric_value:

        response += f"""
# 💰 الإجمالي التقريبي

## {total:,.0f} جنيه سوداني

> ملاحظة: يتم الحساب بضرب الفئة الرقمية في العدد المدخل.
"""

    else:

        response += """
⚠️ لم يتم العثور على قيمة رقمية يمكن حسابها.
"""

    return response


# =========================================================
# العمليات الحسابية المسموحة
# =========================================================

_ALLOWED_OPERATORS = {

    ast.Add: operator.add,

    ast.Sub: operator.sub,

    ast.Mult: operator.mul,

    ast.Div: operator.truediv,

    ast.FloorDiv: operator.floordiv,

    ast.Mod: operator.mod,

    ast.Pow: operator.pow,

    ast.USub: operator.neg,

    ast.UAdd: operator.pos,
}


# =========================================================
# حساب العملية بأمان
# =========================================================

def _safe_calculate(
    node
):

    if isinstance(
        node,
        ast.Expression
    ):

        return _safe_calculate(
            node.body
        )

    if isinstance(
        node,
        ast.Constant
    ):

        if isinstance(
            node.value,
            (int, float)
        ):

            return node.value

        raise ValueError(
            "قيمة غير مسموحة"
        )

    if isinstance(
        node,
        ast.Num
    ):

        return node.n

    if isinstance(
        node,
        ast.UnaryOp
    ):

        operation = (
            _ALLOWED_OPERATORS.get(
                type(node.op)
            )
        )

        if operation is None:

            raise ValueError(
                "عملية غير مسموحة"
            )
            return operation(
            _safe_calculate(
                node.operand
            )
        )

    if isinstance(
        node,
        ast.BinOp
    ):

        operation = (
            _ALLOWED_OPERATORS.get(
                type(node.op)
            )
        )

        if operation is None:

            raise ValueError(
                "عملية غير مسموحة"
            )

        left = _safe_calculate(
            node.left
        )

        right = _safe_calculate(
            node.right
        )

        # حماية من الأسس الكبيرة
        if isinstance(
            node.op,
            ast.Pow
        ):

            if abs(right) > 20:

                raise ValueError(
                    "الأس لا يمكن أن يكون أكبر من 20"
                )

        return operation(
            left,
            right
        )

    raise ValueError(
        "عملية غير مسموحة"
    )


# =========================================================
# الآلة الحاسبة
# =========================================================

def calculator(
    expression=""
):

    if expression is None:

        expression = ""

    expression = str(
        expression
    ).strip()

    if not expression:

        return """
# 🧮 الآلة الحاسبة

اكتب العملية الحسابية التي تريد تنفيذها.

### أمثلة:

50000 + 30000

420000 * 2

500000 - 75000

70000 / 2

(50000 + 30000) * 2
"""

    # دعم رموز الحساب
    expression = expression.replace(
        "×",
        "*"
    )

    expression = expression.replace(
        "÷",
        "/"
    )

    expression = expression.replace(
        "−",
        "-"
    )

    expression = expression.replace(
        ",",
        ""
    )

    # تحويل الأرقام العربية
    arabic_numbers = {

        "٠": "0",
        "١": "1",
        "٢": "2",
        "٣": "3",
        "٤": "4",
        "٥": "5",
        "٦": "6",
        "٧": "7",
        "٨": "8",
        "٩": "9",
    }

    for old, new in arabic_numbers.items():

        expression = expression.replace(
            old,
            new
        )

    try:

        tree = ast.parse(
            expression,
            mode="eval"
        )

        result = _safe_calculate(
            tree
        )

        if (
            isinstance(
                result,
                float
            )
            and result.is_integer()
        ):

            result = int(
                result
            )

        return f"""
# 🧮 نتيجة الآلة الحاسبة

### العملية:

{expression}

### النتيجة:

# {result:,}

💵 جنيه سوداني
"""

    except ZeroDivisionError:

        return """
# ❌ خطأ

لا يمكن القسمة على صفر.
"""

    except Exception:

        return """
# ❌ عملية غير صحيحة

يرجى إدخال عملية حسابية صحيحة.

### مثال:

420000 + 350000

أو:

70000 * 5
"""


# =========================================================
# إحصائيات النظام
# =========================================================

def get_statistics():

    try:

        total_records = len(
            df
        )

        if "وظيفة" in df.columns:

            total_jobs = (
                df["وظيفة"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            total_jobs = 0

        if "نوع_المكافأة" in df.columns:

            total_rewards = (
                df["نوع_المكافأة"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            total_rewards = 0

        if "القسم" in df.columns:

            sections = (
                df["القسم"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            sections = 0

        return f"""
# 📊 لوحة إحصائيات النظام

| البيان | العدد |
|---|---:|
| 📋 إجمالي السجلات | {total_records} |
| 👤 الوظائف المختلفة | {total_jobs} |
| 🎁 أنواع المكافآت | {total_rewards} |
| 🏛 الأقسام | {sections} |

---

## 🏛 مساعد لائحة الحوافز والمكافآت

### جامعة البطانة

📌 البيانات مأخوذة من لائحة المكافآت والحوافز - تعديل 2025م.
"""

    except Exception as error:
        return f"""
# ❌ تعذر استخراج الإحصائيات

الخطأ:

{error}
"""


# =========================================================
# جدول الإحصائيات
# =========================================================

def get_statistics_dataframe():

    try:

        if "وظيفة" in df.columns:

            total_jobs = (
                df["وظيفة"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            total_jobs = 0

        if "نوع_المكافأة" in df.columns:

            total_rewards = (
                df["نوع_المكافأة"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            total_rewards = 0

        if "القسم" in df.columns:

            sections = (
                df["القسم"]
                .dropna()
                .astype(str)
                .nunique()
            )

        else:

            sections = 0

        return pd.DataFrame({

            "البيان": [

                "إجمالي السجلات",

                "الوظائف المختلفة",

                "أنواع المكافآت",

                "الأقسام",
            ],

            "القيمة": [

                len(df),

                total_jobs,

                total_rewards,

                sections,
            ]
        })

    except Exception:

        return pd.DataFrame()


# =========================================================
# تصدير CSV
# =========================================================

def export_csv():

    try:

        export_df = df.copy()

        if "وظيفة_بحث" in export_df.columns:

            export_df = export_df.drop(
                columns=[
                    "وظيفة_بحث"
                ]
            )

        file_path = os.path.join(
            tempfile.gettempdir(),
            "جامعة_البطانة_الحوافز.csv"
        )

        export_df.to_csv(
            file_path,
            index=False,
            encoding="utf-8-sig"
        )

        return file_path

    except Exception:

        return None


# =========================================================
# تصدير Excel
# =========================================================

def export_excel():

    try:

        export_df = df.copy()

        if "وظيفة_بحث" in export_df.columns:

            export_df = export_df.drop(
                columns=[
                    "وظيفة_بحث"
                ]
            )

        file_path = os.path.join(
            tempfile.gettempdir(),
            "جامعة_البطانة_الحوافز.xlsx"
        )

        export_df.to_excel(
            file_path,
            index=False
        )

        return file_path

    except Exception:

        return None


# =========================================================
# الحصول على جميع البيانات
# =========================================================

def get_all_data():

    result = df.copy()

    if "وظيفة_بحث" in result.columns:

        result = result.drop(
            columns=[
                "وظيفة_بحث"
            ]
        )

    return result


# =========================================================
# البحث الشامل
# =========================================================

def global_search(
    query=""
):

    if query is None:

        query = ""

    query = str(
        query
    ).strip()

    if not query:

        return get_all_data()

    normalized_query = normalize_text(
        query
    )

    result_rows = []

    for _, row in df.iterrows():

        found = False

        for value in row.tolist():

            if (
                normalized_query
                in normalize_text(value)
            ):

                found = True

                break

        if found:

           result_rows.append(
                row
            )

    if not result_rows:

        return pd.DataFrame(
            columns=[
                column
                for column in df.columns
                if column != "وظيفة_بحث"
            ]
        )

    result = pd.DataFrame(
        result_rows
    )

    if "وظيفة_بحث" in result.columns:

        result = result.drop(
            columns=[
                "وظيفة_بحث"
            ]
        )

    return result


# =========================================================
# معلومات النظام
# =========================================================

def system_info():

    try:

        total_jobs = (
            df["وظيفة"]
            .dropna()
            .astype(str)
            .nunique()
            if "وظيفة" in df.columns
            else 0
        )

        total_rewards = (
            df["نوع_المكافأة"]
            .dropna()
            .astype(str)
            .nunique()
            if "نوع_المكافأة" in df.columns
            else 0
        )

        return f"""
# 🏛 معلومات النظام

## اسم النظام

مساعد لائحة الحوافز والمكافآت

## الجامعة

جامعة البطانة

## إصدار اللائحة

تعديل 2025م

---

## 📊 معلومات البيانات

عدد السجلات:

{len(df)}

عدد الوظائف المختلفة:

{total_jobs}

عدد أنواع المكافآت:

{total_rewards}

---

## 🔐 معلومات المستخدم

اسم المستخدم:

admin

رمز الدخول:

1234

---

### 🧮 الأدوات المتوفرة

🔎 البحث عن الوظائف والمكافآت

🧮 حساب الاستحقاق

🧮 الآلة الحاسبة

📊 الإحصائيات

🌐 البحث الشامل

📥 تصدير CSV

📊 تصدير Excel
"""

    except Exception as error:

        return f"""
# 🏛 مساعد لائحة الحوافز والمكافآت

## جامعة البطانة

حدث خطأ أثناء قراءة معلومات النظام:

{error}
"""


# =========================================================
# اختبار أن الدوال موجودة
# =========================================================

def test_functions():

    return {

        "login":
            callable(login),

        "logout":
            callable(logout),

        "search_jobs":
            callable(search_jobs),

        "search_by_job_and_reward":
            callable(
                search_by_job_and_reward
            ),

        "calculate_entitlement":
            callable(
                calculate_entitlement
            ),

        "calculator":
            callable(
                calculator
            ),

        "get_statistics":
            callable(
                get_statistics
            ),

        "get_statistics_dataframe":
            callable(
                get_statistics_dataframe
            ),

        "export_csv":
            callable(
                export_csv
            ),

        "export_excel":
            callable(
                export_excel
            ),

        "global_search":
            callable(
                global_search
            ),

        "system_info":
            callable(
                system_info
            ),
    }


# =========================================================
# نهاية الملف
# ========================================================= 
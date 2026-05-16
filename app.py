import streamlit as st
import random
from fractions import Fraction
import re
import math

# --- 頁面基本設定 ---
st.set_page_config(page_title="HK小學數學練習器", page_icon="🎓", layout="wide")

# ==========================================
# 1. 核心工具函數 (Utility Functions)
# ==========================================
def format_money(cents):
    y = cents // 10
    j = cents % 10
    return f"{y}元{j}角" if j != 0 else f"{y}元"

def parse_mixed_fraction(s):
    s = s.replace("又", "+").replace(" ", "+").strip()
    s = re.sub(r'\++', '+', s)  
    if "+" in s:
        parts = s.split("+")
        if len(parts) == 2 and "/" in parts[1]:
            return Fraction(int(parts[0])) + Fraction(parts[1])
        return sum(Fraction(p) for p in parts)
    return Fraction(s)

def fmt_decimal(val):
    """將小數轉為字串並移除無效的末尾0"""
    return f"{float(val):.4f}".rstrip('0').rstrip('.')

def get_lcm(a, b):
    return abs(a * b) // math.gcd(a, b)

# ==========================================
# 2. 各年級題目生成邏輯 (Topic Generators)
# ==========================================

# --- 小一 ---
def hks1_1(): return f"{random.randint(1, 9)} + {random.randint(1, 9)}", random.randint(1, 9) + random.randint(1, 9) # 範例簡化，實務上可對應原有邏輯
def hks1_2():
    a = random.randint(1, 18)
    b = random.randint(1, min(a, 9))
    return f"{a} - {b}", a - b
def hks1_3():
    res = random.randint(10, 100)
    a = random.randint(1, res - 1)
    return f"{a} + {res - a}", res
def hks1_4():
    res = random.randint(10, 100)
    a = random.randint(1, res - 2)
    b = random.randint(1, res - a - 1)
    return f"{a} + {b} + {res - a - b}", res
def hks1_5():
    a = random.randint(10, 99)
    b = random.randint(1, a)
    return f"{a} - {b}", a - b

# --- 小二 ---
def hks2_1():
    res = random.randint(100, 999)
    a, b = random.randint(10, 400), random.randint(10, 400)
    return f"{a} + {b} + {res-a-b}", res
def hks2_2():
    a, ans = random.randint(20, 99), random.randint(1, 19)
    return f"{a} - ? = {ans}", a - ans
def hks2_3():
    a = random.randint(50, 99)
    b, c = random.randint(1, 20), random.randint(1, 20)
    return f"{a} - {b} - {c}", a - b - c
def hks2_4():
    a, b = random.randint(0, 10), random.randint(0, 10)
    return f"{a} × {b}", a * b
def hks2_5():
    a = random.randint(100, 999)
    b = random.randint(10, a - 1)
    return f"{a} - {b}", a - b
def hks2_6():
    a = random.randint(10, 500)
    b, c = random.randint(1, 100), random.randint(1, 100)
    return f"{a} + {b} - {c}", a + b - c
def hks2_7():
    c1, c2 = random.randint(50, 200), random.randint(10, 40)
    return f"{format_money(c1)} - {format_money(c2)}", c1 - c2
def hks2_8():
    ans, b = random.randint(1, 10), random.randint(1, 10)
    return f"{ans * b} ÷ {b}", ans

# --- 小三 ---
def hks3_1():
    a, b = random.randint(10, 99), random.randint(2, 9)
    return f"{a} × {b}", a * b
def hks3_2():
    a, b = random.randint(100, 999), random.randint(2, 9)
    return f"{a} × {b}", a * b
def hks3_3():
    b = random.randint(2, 9); a = random.randint(10, 99)
    ans, rem = divmod(a, b)
    return f"{a} ÷ {b}", f"{ans}...{rem}" if rem > 0 else f"{ans}"
def hks3_4():
    b = random.randint(2, 9); a = random.randint(100, 999)
    ans, rem = divmod(a, b)
    return f"{a} ÷ {b}", f"{ans}...{rem}" if rem > 0 else f"{ans}"
def hks3_5():
    a, b, c = random.randint(100, 500), random.randint(100, 500), random.randint(10, 90)
    return f"{a} + {b} - {c}", a + b - c
def hks3_6():
    d = random.randint(3, 12)
    if random.random() < 0.3:
        a = random.randint(1, d - 1)
        return f"{a}/{d} + {d-a}/{d}", "1"
    else:
        a = random.randint(1, d - 2); b = random.randint(1, d - a - 1)
        return f"{a}/{d} + {b}/{d}", f"{a+b}/{d}"
def hks3_7():
    d = random.randint(3, 12); a = random.randint(2, d - 1); b = random.randint(1, a - 1)
    return f"{a}/{d} - {b}/{d}", f"{a-b}/{d}"

# ==========================================
# 3. 模組化課程與映射配置 (Curriculum Mapping)
# ==========================================
# 這裡將「課題名稱」與「對應的生成函數」直接綁定，未來擴充極為簡單！
MAP_S1 = {
    "一位數加法": hks1_1, "減法": hks1_2, "兩位數加法": hks1_3, 
    "三個數的加法": hks1_4, "兩位數減法": hks1_5
}
MAP_S2 = {
    "三個數的加法": hks2_1, "兩位數減法": hks2_2, "三個數的減法": hks2_3, 
    "基本乘法": hks2_4, "三位數減法": hks2_5, "三個數的加減混合": hks2_6, 
    "貨幣運算": hks2_7, "基本除法": hks2_8
}
MAP_S3 = {
    "乘法(兩位數 × 一位數)": hks3_1, "乘法(三位數 × 一位數)": hks3_2, 
    "除法(兩位數 ÷ 一位數)": hks3_3, "除法(三位數 ÷ 一位數)": hks3_4, 
    "三個數的加減混合運算": hks3_5, "分數加法": hks3_6, "分數減法": hks3_7
}

# 總課程選單目錄
CURRICULUM_MAP = {
    "小一": MAP_S1,
    "小二": MAP_S2,
    "小三": MAP_S3
    # 小四、小五、小六可以依此類推放入對應的字典映射
}

# ==========================================
# 4. 練習器主程式介面 (Streamlit UI Main)
# ==========================================
if 'current_q' not in st.session_state:
    st.session_state.update({
        'current_q': "請選取課題後點擊「開始出題」", 
        'current_ans': 0, 'current_topic': "", 'feedback': "", 
        'score': 0, 'total': 0, 'has_submitted': False, 'q_counter': 0, 'first_run': True
    })

with st.sidebar:
    st.title("🎓 課程設定")
    grade = st.selectbox("選擇年級", list(CURRICULUM_MAP.keys()), key="grade_selector")
    
    # 從對應的映射字典讀取課題清單
    available_topics = list(CURRICULUM_MAP[grade].keys())
    selected_topics = [t for t in available_topics if st.checkbox(t, value=False, key=f"cb_{grade}_{t}")]
    
    if st.button("🔄 重新開始"):
        st.session_state.update({'score': 0, 'total': 0, 'current_q': "請選取課題後點擊「開始出題」", 'has_submitted': False, 'q_counter': 0, 'first_run': True, 'feedback': ""})
        st.rerun()

st.title("🇭🇰 香港小學數學練習系統")
c1, c2 = st.columns(2)
c1.metric("練習年級", grade)
c2.metric("得分率", f"{st.session_state.score} / {st.session_state.total}")

st.write("📖 當前練習範圍：")
if selected_topics:
    topics_html = "".join([f'<span style="background-color: #e1f5fe; color: #01579b; padding: 2px 8px; border-radius: 10px; margin-right: 5px; font-size: 0.8em; border: 1px solid #b3e5fc;">{t}</span>' for t in selected_topics])
    st.markdown(topics_html, unsafe_allow_html=True)
else:
    st.info("尚未選擇任何課題。")

st.divider()

display_q = st.session_state.current_q
if st.session_state.current_topic != "" and "?" not in display_q:
    display_q = f"{display_q} = ?"

st.subheader(f"🎯 題目：{display_q}")

is_money_q = (st.session_state.current_topic == "貨幣運算")

with st.form(key=f"ans_form_{st.session_state.q_counter}", clear_on_submit=False):
    if is_money_q:
        st.caption("💡 提示：若答案為 0 角，可不填")
        mc1, mc2 = st.columns(2)
        u_yuan = mc1.number_input("元", min_value=0, step=1, value=None, key=f"yuan_{st.session_state.q_counter}")
        u_jiao = mc2.number_input("角", min_value=0, max_value=9, step=1, value=None, key=f"jiao_{st.session_state.q_counter}")
    else:
        st.caption("💡 格式提示：\n- 分數：(分子)/(分母) 如 `3/4`\n- 帶分數：整數與分數間加空格 如 `1 2/3`\n- 餘數：使用 `...` 如 `10...2`")
        u_input = st.text_input("在此輸入答案：", key=f"input_{st.session_state.q_counter}")
    
    submit_btn = st.form_submit_button("提交答案", use_container_width=True)
    
    if submit_btn:
        if st.session_state.current_topic == "":
            st.warning("請先開始出題！")
        else:
            correct = False
            user_ans_raw = str(u_input).strip() if not is_money_q else ""
            standard_ans = str(st.session_state.current_ans)

            if is_money_q:
                val_y = u_yuan if u_yuan is not None else 0
                val_j = u_jiao if u_jiao is not None else 0
                if (val_y * 10 + val_j) == st.session_state.current_ans: correct = True
                ans_str = format_money(st.session_state.current_ans)
            else:
                if standard_ans == "1": correct = (user_ans_raw == "1")
                elif "/" in standard_ans or "/" in user_ans_raw:
                    try:
                        if parse_mixed_fraction(user_ans_raw) == parse_mixed_fraction(standard_ans): correct = True
                    except: pass
                elif "..." in standard_ans: correct = (user_ans_raw.replace(" ", "") == standard_ans.replace(" ", ""))
                else:
                    try:
                        if float(user_ans_raw) == float(standard_ans): correct = True
                    except: correct = (user_ans_raw == standard_ans)
                ans_str = standard_ans

            if correct:
                st.session_state.feedback = "✅ 答對了！"
                if not st.session_state.has_submitted: st.session_state.score += 1
            else:
                st.session_state.feedback = f"❌ 錯誤，正確答案是：{ans_str}"
            
            if not st.session_state.has_submitted:
                st.session_state.total += 1
                st.session_state.has_submitted = True

if st.session_state.feedback:
    if "✅" in st.session_state.feedback: st.success(st.session_state.feedback)
    else: st.error(st.session_state.feedback)

if st.session_state.has_submitted or st.session_state.first_run:
    btn_text = "下一題 ➡️" if not st.session_state.first_run else "開始出題 ➡️"
    if st.button(btn_text, use_container_width=True, key="next_q"):
        if not selected_topics:
            st.error("請至少選取一個課題！")
        else:
            topic = random.choice(selected_topics)
            
            # 核心重構優化點：直接由字典動態調用對應函數，免去大量的 if-elif 判斷
            q, a = CURRICULUM_MAP[grade][topic]()
            
            st.session_state.update({
                'current_q': q, 'current_ans': a, 'current_topic': topic,
                'feedback': "", 'has_submitted': False, 'first_run': False,
                'q_counter': st.session_state.q_counter + 1
            })
            st.rerun()
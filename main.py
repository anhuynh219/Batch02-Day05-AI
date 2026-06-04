import json
import os
import numpy as np
from datetime import datetime
from dotenv import load_dotenv

# Import SDK mới của Google
from google import genai
from google.genai import types

# Load biến môi trường
load_dotenv(dotenv_path=".env")
api_key = os.getenv("GEMINI_API_KEY")

# Khởi tạo Client theo chuẩn SDK mới
client = genai.Client(api_key=api_key)

# ==========================================
# COMPONENT 1: LOAD DỮ LIỆU & XỬ LÝ THỜI GIAN
# ==========================================

def load_events(file_path="data/events_data.json"):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def time_to_obj(time_str):
    return datetime.strptime(time_str, "%H:%M:%S").time()

def is_time_overlap(start1, end1, start2, end2):
    return max(start1, start2) < min(end1, end2)

def filter_events_by_time(events, user_start, user_end, blocked_intervals, history_array):
    valid_events = []
    user_start_t = time_to_obj(user_start)
    user_end_t = time_to_obj(user_end)
    blocked_t = [(time_to_obj(b["start"]), time_to_obj(b["end"])) for b in blocked_intervals]
    booked_ids = [event["id"] for event in history_array]

    for event in events:
        if event["id"] in booked_ids:
            continue
            
        ev_start = time_to_obj(event["time_start"])
        ev_end = time_to_obj(event["time_end"])

        if ev_start >= user_start_t and ev_end <= user_end_t:
            is_blocked = False
            for b_start, b_end in blocked_t:
                if is_time_overlap(ev_start, ev_end, b_start, b_end):
                    is_blocked = True
                    break
            
            if not is_blocked:
                valid_events.append(event)
                
    return valid_events

# ==========================================
# COMPONENT 2: RETRIEVAL EMBEDDING & AI AGENT (CÚ PHÁP MỚI)
# ==========================================

def get_embedding(text, task_type="RETRIEVAL_DOCUMENT"):
    """
    Gọi Gemini API (SDK mới) để lấy Vector Embedding.
    """
    try:
        response = client.models.embed_content(
            model='text-embedding-004',
            contents=text,
            config=types.EmbedContentConfig(task_type=task_type)
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"[!] Lỗi embedding: {e}")
        return None

def cosine_similarity(v1, v2):
    return np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))

def retrieve_top_events(valid_events, user_preferences, top_k=2):
    """Tìm Top K sự kiện khớp sở thích."""
    if not valid_events:
        return []

    # Embedding Query của User
    user_vector = get_embedding(user_preferences, task_type="RETRIEVAL_QUERY")
    if not user_vector:
        return valid_events[:top_k]

    scored_events = []
    for event in valid_events:
        # Embedding Document (Description)
        event_vector = get_embedding(event["description"], task_type="RETRIEVAL_DOCUMENT")
        if event_vector:
            score = cosine_similarity(user_vector, event_vector)
            scored_events.append((score, event))
    
    scored_events.sort(key=lambda x: x[0], reverse=True)
    return [event for score, event in scored_events[:top_k]]

def get_ai_recommendation_with_rag(valid_events, user_preferences, history_array):
    """LLM Generate nội dung dựa trên kết quả RAG."""
    if not valid_events:
        return {
            "status": "failure",
            "message": "Hiện tại không còn sự kiện nào phù hợp với khung giờ và ràng buộc thời gian của bạn."
        }

    top_matched_events = retrieve_top_events(valid_events, user_preferences, top_k=2)

    available_events_str = "\n".join(
        [f"- ID: {ev['id']} | Tên: {ev['name']} | Khung giờ: {ev['time_start']} đến {ev['time_end']} | Mô tả: {ev['description']}" for ev in top_matched_events]
    )
    
    booked_events_str = "Trống" if not history_array else "\n".join([f"- ID: {ev['id']} | Tên: {ev['name']}" for ev in history_array])

    prompt = f"""
    Bạn là một trợ lý ảo thiết kế lịch trình chuyên nghiệp tại Vinhome Oceanpark.
    
    THÔNG TIN ĐẦU VÀO:
    1. Sở thích của khách: "{user_preferences}"
    2. Các sự kiện khách ĐÃ CHỌN: {booked_events_str}
    3. Các sự kiện KHẢ DỤNG & PHÙ HỢP NHẤT:
    {available_events_str}
    
    YÊU CẦU ĐẦU RA:
    - Hãy giao tiếp thật tự nhiên, đóng vai trò trợ lý để tư vấn các sự kiện KHẢ DỤNG ở trên.
    - Cung cấp rõ Mã ID sự kiện (VD: VINPQ001) để khách hàng chọn.
    """

    try:
        # Gọi API tạo văn bản (Cú pháp SDK mới)
        response = client.models.generate_content(
            model='gemini-2.5-flash',
            contents=prompt,
        )
        return {
            "status": "success",
            "message": response.text
        }
    except Exception as e:
        return {
            "status": "error",
            "message": f"Lỗi khi gọi API sinh văn bản: {str(e)}"
        }

# ==========================================
# WORKFLOW CHÍNH ĐỂ TEST
# ==========================================
if __name__ == "__main__":
    all_events = load_events()
    history_array = [] 
    
    # Giả lập input (Bắt buộc phải lọt qua cửa lọc thời gian mới gọi API)
    user_start_time = "08:00:00"
    user_end_time = "14:00:00"
    blocked_times = [{"start": "11:30:00", "end": "12:30:00"}]
    user_pref = "Gia đình tôi có trẻ con, tôi muốn tìm các hoạt động nhẹ nhàng, ưu tiên xem thú hoặc biểu diễn."

    print("--- BƯỚC 1: BACKEND LỌC THỜI GIAN ---")
    valid_events = filter_events_by_time(
        all_events, user_start_time, user_end_time, blocked_times, history_array
    )
    print(f"Số sự kiện hợp lệ về thời gian: {len(valid_events)}")
    
    print("\n--- BƯỚC 2: AI AGENT RETRIEVAL & GỢI Ý ---")
    agent_response = get_ai_recommendation_with_rag(valid_events, user_pref, history_array)
    
    if agent_response["status"] == "success":
        print(agent_response["message"])
    else:
        print(f"Hệ thống thông báo: {agent_response['message']}")
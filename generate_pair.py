import litellm
import json
import utils
import re

def generate_pair(content, model="gemini/gemini-1.5-flash"):
    num = 3
    prompt_prefix = f"""
    Tạo ra {num} cặp câu hỏi và trả lời, trong đó câu trả lời được trích nguyên văn và là 1 phần của bài viết dưới đây, câu trả lời phải chứa đầy đủ mọi nội dung và không giới hạn độ dài
Format các cặp này dưới định dạng json chứa trong tag "question" và "answer" và chỉ trả kết quả là json này không add thêm bất cứ thứ gì khác.

---
    """
    prompt = prompt_prefix + content
    
    
    
    response = litellm.completion(
        model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant to provide dataset for model finetuning"},
            {"role": "user", "content": prompt},
        ],
    )
    out = response.choices[0].message.content
    ## strip json content out of the markdown
    out = re.sub(r"```json\n(.*?)\n```", r"\1", out, flags=re.DOTALL)
    results = json.loads(out)
    return results




if __name__ == "__main__":
    content = """
    Acid uric là gì?
Acid uric là một hợp chất dị vòng của cacbon, oxi, hydro và nitơ, có công thức C5H4N4O3 được tạo thành trong cơ thể do quá trình thoái giáng các nhân purin. Tiếp theo chúng được hòa tan trong máu và cuối cùng chúng được đưa đến thận và thải ra ngoài qua nước tiểu.

Acid uric là một hợp chất lần đầu tiên được phân lập từ sỏi thận vào năm 1776 bởi nhà hóa học người Thụy Điển Carl Wilhelm Scheele. Nhà hóa học người Ukraina Ivan Horbaczewski lần đầu tiên tổng hợp axit uric bằng cách nấu chảy urê bằng glycine vào năm 1882

Chỉ số acid uric có khả năng quyết định chẩn đoán về bệnh gout mà bệnh nhân có mắc phải hay không, phản ảnh rõ mức độ nghiêm trọng người bệnh đang ở giai đoạn nào.

Acid uric là sản phẩm chuyển hóa các chất đạm được tìm thấy ở trong nhiều thực phẩm như phủ tạng động vật, đậu Hà Lan, cá biển hoặc những đồ uống có cồn như rượu, bia,...
Axit uric cao có thể do quá trình tăng cung cấp, tăng tạo hoặc giảm thải trừ axit uric qua thận hoặc hỗn hợp cả hai quá trình này. Khi nồng độ axit uric tăng cao kéo dài trong máu có thể dẫn đến một dạng viêm khớp được biết đến với tên bệnh gout. Các hạt lắng đọng trong và xung quanh các khớp dẫn đến hậu quả viêm, sưng và đau khớp, lắng đọng dưới da tạo nên các hạt tophi, có thể tạo sỏi thận và suy thận.
    """
    
    utils.set_api_key_config()
    results = generate_pair(content)
    
    for result in results:
        print(result)
    
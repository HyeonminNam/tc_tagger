import json
import re
from pykospacing import spacing # 설치 방법 : pip install git+https://github.com/haven-jeon/PyKoSpacing.git

class Preprocessing_Insta () :
    
    def __init__(self):
        self.escape_code = ['\n', '\xa0', '\"', '\'', '\t', '\r', '\$', '\\', '\u200d']
        return
    
    # hashtag 추출(#포함)
    def extract_hashtag(self, content) :
        hashtag_list = re.findall('\#[\w가-힣a-zA-Z0-9]*', str(content))
        if hashtag_list:
            return hashtag_list
        else :
            return ''
    
    # post 추출
    def extract_post(self, content) :  
        post = re.sub('\#[\w가-힣a-zA-Z0-9]*',"",str(content)) 
        post = self.del_escape(post)
        post = re.sub("\@[\w가-힣a-zA-Z0-9]*","",post)   
        return post #string type

    # 태그된 userID 추출
    def extract_tagged_userID(self, content) : #태그된 userID 추출의 경우 hashtag 추출과 달리 @를 제거해준 값 리턴 
        re_content = re.findall('\@[\w가-힣a-zA-Z0-9]*', str(content))
        tmp = []
        for userID in re_content:
            tmp.append(re.sub("@","",userID))
        return tmp

    # hashtag(#) 제거
    def remove_hash(self, hashtag_list) :
        for hashtag in hashtag_list:
            tmp = []
            for j in  hashtag:
                tmp.append(re.sub("#","",j))
        return tmp
    
    # pykospacing패키지를 사용한 띄어쓰기 처리
    def auto_spacing(self, content) :
        return spacing(content)
        
    # Escape Code 처리
    def del_escape(self, content):
        for e in self.escape_code:
            content = content.replace(e, ' ')
        return content
    
    # emoji 삭제
    def del_emoji(self, content) :
        only_BMP_pattern = re.compile("["
        u"\U00010000-\U0010FFFF"  #BMP characters 이외
                           "]+", flags=re.UNICODE)
        return only_BMP_pattern.sub(r'', content)
    
    # content list 전처리
    def preprocess_content(self, content_list, spacing = False) :        
        post_list =[]
        hashtag_list= []         
        for content in content_list :
            original_post = self.extract_post(content)
            if spacing :
                post_list.append(self.auto_spacing(original_post))
            else :
                post_list.append(original_post)
            hashtag_list.append(self.remove_hash(self.extract_hashtag(content)))
        return post_list, hashtag_list
    
if __name__ == "__main__":
    content_list = ['다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt','럽스타 그자체❤❤ #럽스타그램 #운동하는커플 #연산동pt']
    test_class = Preprocessing_Insta()
    post_ls, hashtag_ls = test_class.preprocess_content(content_list, spacing= True)
    print(post_ls)
    print(hashtag_ls)
    print("-----------------------------------------------------------------------------------------------")
    print("*************이모지 삭제 활용 예시*************")
    for post in post_ls : 
        print(test_class.del_emoji(post))
    
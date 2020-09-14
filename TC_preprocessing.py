#-*- coding: utf-8 -*-
import os
import sys
sys.path.append(os.path.dirname(__file__))
import re
import emoji
# from pykospacing import spacing # 설치 방법 : pip install git+https://github.com/haven-jeon/PyKoSpacing.git

class Preprocessing() :
    
    def __init__(self):
        self.escape_code = ['\n', '\xa0', '\"', '\'', '\t', '\r', '\$', '\\', '\u200d']
        self.emoji_dic = emoji.UNICODE_EMOJI
        self.emoji_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.re_emoji = re.compile('|'.join(re.escape(p) for p in self.emoji_list if p != '\u200d|\u200c'))
        return
    
    # hashtag 추출(#포함)
    def extract_hashtag(self, text) :
        hashtag_list = re.findall('\#[\w가-힣a-zA-Z0-9]*', str(text))
        if hashtag_list:
            return hashtag_list
        else :
            return ''
    
    # post 추출
    def extract_post(self, text) :  
        post = re.sub('\#[\w가-힣a-zA-Z0-9]*',"",str(text)) 
        post = self.del_escape(post)
        post = re.sub("\@[\w가-힣a-zA-Z0-9]*","",post)   
        return post #string type

    # 태그된 userID 추출
    def extract_tagged_userID(self, text) : #태그된 userID 추출의 경우 hashtag 추출과 달리 @를 제거해준 값 리턴 
        re_text = re.findall('\@[\w가-힣a-zA-Z0-9]*', str(text))
        userID_list= []
        for userID in re_text:
            userID_list.append(re.sub("@","",userID))
        return userID_list

    # hashtag(#) 제거
    def remove_hash(self, hashtag_list) :
        for hashtag in hashtag_list:
            tmp = []
            for j in  hashtag:
                tmp.append(re.sub("#","",j))
        return tmp
    
    # # pykospacing패키지를 사용한 띄어쓰기 처리
    # def auto_spacing(self, text) :
    #     return spacing(text)
        
    # Escape Code 처리
    def del_escape(self, text):
        for e in self.escape_code:
            text = text.replace(e, ' ')
        return text
    
    # emoji 삭제
    def del_emoji(self, text) :
        return self.re_emoji.sub(r'', text)
    
    # text list 전처리
    def preprocess_text(self, text_list, sub_hash = False) :        
        post_list =[]
        hashtag_list= []         
        for text in text_list :
            original_post = self.extract_post(text)
            # if spacing :
            #     # post_list.append(self.auto_spacing(original_post))
            #     pass
            # else :
            post_list.append(original_post)
            if sub_hash :
                hashtag_list.append(self.remove_hash(self.extract_hashtag(text)))
            else :
                hashtag_list.append(self.extract_hashtag(text))
        return post_list, hashtag_list
    
if __name__ == "__main__":
    text_list = ['다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt','럽스타 그자체❤❤ #럽스타그램 #운동하는커플 #연산동pt']
    test_class = Preprocessing()
    post_ls, hashtag_ls = test_class.preprocess_text(text_list)
    print(post_ls)
    print(hashtag_ls)
    print("-----------------------------------------------------------------------------------------------")
    print("*************이모지 삭제 활용 예시*************")
    for post in post_ls : 
        print(test_class.del_emoji(post))
    
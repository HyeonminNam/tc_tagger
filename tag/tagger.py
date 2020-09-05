from konlpy.tag import Okt
import emoji
import re


class Tagger():

    def __init__(self):
        emojis_list = map(lambda x: ''.join(x.split()), emoji.UNICODE_EMOJI.keys())
        self.r = re.compile('|'.join(re.escape(p) for p in emojis_list))
       

    def _emoticon(self, result):
        emo_lst = []
        for idx, (token, _) in enumerate(result):
            if re.search(self.r, token):
                lst = [(x, 'Emoji') for x in token]
                emo_lst.append((idx, lst))
        emo_lst.reverse()
        for idx, emo in emo_lst:
            result.pop(idx)
            result[idx:idx] = emo
        return result
    
    def _hashtag(self, result):
        for idx, (token, tag) in enumerate(result):
            if tag == 'Hashtag':
                phrase = okt.phrases(token[1:])[0]
                new_token = re.sub(phrase, ' '+phrase+' ' , token[1:]).strip().split()
                h = []
                for x in new_token:
                    if x == phrase:
                        h.append((x, 'Hashtag_Noun'))
                    else:
                        tmp = okt.pos(x)
                        for token, tag in tmp:
                            h.append((token, 'Hashtag_'+tag))         
                result[idx] = tuple(h)
        return result

    def tag(self, text):
        okt = Okt()
        result = okt.pos(text)
        result = self._emoticon(result)
        result = self._hashtag(result)
        return result

            
if __name__ == "__main__":
    text = '다이어트 해야되는데...😂😂\n.\n.\n.\n#멋짐휘트니스연산점 #연산동pt'
    text2 = '럽스타 그자체❤❤ #럽스타그램 #운동하는커플 #연산동pt'
    okt = Okt()
    threecow = Tagger()
    print('='*100)
    print('\nOkt : ', okt.pos(text2))
    print('\nThreecow : ', threecow.tag(text2))
    print('\n', '='*100)

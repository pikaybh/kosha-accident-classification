# Internal Modules
from ._openai import call_openai_api
from .utils.templateloader import PromptTemplate
# External Modules
import logging

# Root 
logger_name = "gpt.zsl"
logger = logging.getLogger(logger_name)
logger.setLevel(logging.DEBUG)
# File Handler
file_handler = logging.FileHandler(f'logs/{logger_name}.log', encoding='utf-8-sig')
file_handler.setLevel(logging.DEBUG)
file_handler.setFormatter(logging.Formatter(r'%(asctime)s [%(name)s, line %(lineno)d] %(levelname)s: %(message)s'))
logger.addHandler(file_handler)
# Stream Handler
stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(logging.Formatter(r'%(message)s'))
logger.addHandler(stream_handler)


SYSTEM_MSG : str = """
당신은 사고 사례를 특정 작업 유형으로 분류하는 고급 AI입니다. 사고 사례의 설명을 받게 되면, 이를 사전에 정의된 작업 유형에 따라 분류하는 것이 당신의 임무입니다. 용어와 문맥을 이해하여 최상의 분류를 수행하세요. 대답은 각설하고 해당하는 작업 유형만 답합니다. 다음은 분류해야 할 작업 유형 목록입니다:

- 가설전기 작업
- 비계 조립 및 해체 작업
- 낙하물방지망 및 방호선반 작업
- 타워크레인 설치 및 해체 작업
- 건설용 리프트 설치 및 해체 작업
- 굴착 및 발파 작업
- 흙막이 지보공 작업
- 거푸집동바리 작업
- 철근 작업
- 콘크리트 타설 작업
- 작업발판 일체형 거푸집 작업
- 철골 작업
- PC 작업
- 외부마감 작업
- 내부마감 작업
- 기계식주차장 설치 작업
- 엘리베이터 설치 작업
- 기계실 설비 작업
- *지상높이가 31미터 이상인 건축물 참고
- *깊이 10미터 이상인 굴착공사 참고
- 가설작업
- 가설도로 작업
- 파일 작업
- 구조물 작업
- 거더작업(PSC I형거더)
- FCM(Free Cantilever method)
- ILM(Incremental Launching Method)
- FSM(Full Staging Method)
- PSM(Precast Segment Method)
- 강교(Steel Box)
- 주탑 및 케이블 설치작업(현수교, 사장교 및 Extradosed교)
- 비계작업
- 갱구부 또는 수직구 굴착작업
- 플랜트 설치작업
- 터널 발파작업
- 버럭 처리작업
- 숏크리트 작업
- 강지보공 작업
- 락볼트 작업
- 터널 방수 및 철근배근 작업
- 라이닝 콘크리트 작업
- 기타 기계설비 설치작업
- 가체절(가물막이) 작업
- 배치플랜트 작업
- 기초처리 작업
- 본댐 기계설비 작업
- 공도교 작업
- 복공 설치 및 해체 작업
"""
USER_MSG : str = """
다음은 적절한 작업 유형으로 분류해야 할 사고 사례 설명입니다:

<CASE>

주어진 사고 사례를 위의 작업 유형 중 하나로 분류하세요.
"""

"""
def main() -> None:
    logger.info(call_openai_api(PromptTemplate.message_loader(system_msg=SYSTEM_MSG, user=USER_MSG.replace("<CASE>", "2014년 1월 2일 종로구 필운동 공사현장에서 설치되어 있는 간판을 칠하기위해 사다리를\n오르다 미끄러 떨어져 발을 다침."))))
"""

def classify_case(case_description: str) -> str:
    response = call_openai_api(PromptTemplate.message_loader(system_msg=SYSTEM_MSG, user=USER_MSG.replace("<CASE>", case_description)))
    return response.strip()

def main() -> None:
    case = "2014년 1월 2일 종로구 필운동 공사현장에서 설치되어 있는 간판을 칠하기위해 사다리를\n오르다 미끄러 떨어져 발을 다침."
    logger.info(classify_case(case))

# Main
if __name__ == '__main__':
    main()

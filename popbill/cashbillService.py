# -*- coding: utf-8 -*-
# Module for Popbill Cashbill API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : John Yohan (yhjeong@linkhub.co.kr)
# Written : 2015-03-24
# Thanks for your interest.

from .base import PopbillBase,PopbillException

class CashbillService(PopbillBase):
    """ 팝빌 현금영수증 API Service Implementation. """

    def __init__(self,LinkID,SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """

        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("140")

    def getURL(self, CorpNum, UserID, ToGo):
        """ 팝빌 현금영수증 관련 URL 
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌 회원아이디
                ToGo : 현금영수증 관련 기능 지정 문자.(TBOX : 임시문서함, PBOX : 매출문서함)
            return
                30초 보안 토큰을 포함한 url
            raise 
                PopbillException
        """

        result = self._httpget('/Cashbill?TG=' + ToGo, CorpNum, UserID)

        return result.url

    def getUnitCost(self, CorpNum):
        """ 현금영수증 발행단가 확인.
            args
                CorpNum : 팝빌회원 사업자번호
            return
                발행단가 by float
            raise 
                PopbillException
        """

        result = self._httpget('/Cashbill?cfg=UNITCOST', CorpNum)

        return float(result.unitCost)

    def checkMgtKeyInUse(self, CorpNum, MgtKey):
        """ 파트너 문서관리번호 사용여부 확인.
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호(최대 24자리, 숫자, 영문,'-','_'로 구성)
            return
                사용 여부 by True/False
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        try:
            result = self._httpget('/Cashbill/' + MgtKey, CorpNum)
            
            return result.itemKey != None and result.itemKey != ""

        except PopbillException as PE:
            if PE.code == -14000003:
                return False
            raise PE

    def register(self, CorpNum, cashbill, UserID = None):
        """ 현금영수증 등록
            args
                CorpNum : 팝빌회원 사업자번호
                cashbill : 등록할 현금영수증 object. made with Cashbill(...)
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if cashbill == None:
            raise PopbillException(-99999999,"현금영수증 정보가 입력되지 않았습니다.")

        postData = self._stringtify(cashbill)

        return self._httppost('/Cashbill',postData,CorpNum,UserID)


    def update(self, CorpNum, MgtKey, cashbill, UserID = None):
        """ 수정
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 원본 현금영수증 문서관리번호
                cashbill : 수정할 현금영수증 object. made with Cashbill(...)
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if cashbill == None:
            raise PopbillException(-99999999,"현금영수증 정보가 입력되지 않았습니다.")   

        postData = self._stringtify(cashbill)

        return self._httppost('/Cashbill/'+ MgtKey, postData, CorpNum, UserID, "PATCH")


    def issue(self, CorpNum, MgtKey, Memo = None, UserID = None):
        """ 발행
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 원본 현금영수증 문서관리번호
                Memo : 발행 메모
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        
        postData = ""
        req = {}

        if Memo != None or Memo != '':
            req["memo"] = Memo
            
        postData = self._stringtify(req)

        return self._httppost('/Cashbill/' + MgtKey, postData, CorpNum, UserID, "ISSUE")

    def cancelIssue(self, CorpNum, MgtKey, Memo = None, UserID = None):
        """ 발행취소
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 원본 현금영수증 문서관리번호
                Memo : 발행취소 메모
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        postData = ""
        req = {}

        if Memo != None or Memo != '':
            req["memo"] = Memo
            
        postData = self._stringtify(req)

        return self._httppost('/Cashbill/' + MgtKey, postData, CorpNum, UserID, "CANCELISSUE")

    def delete(self, CorpNum, MgtKey, UserID = None):
        """ 삭제
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 원본 현금영수증 문서관리번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httppost('/Cashbill/' + MgtKey,'', CorpNum, UserID, "DELETE")

    def getInfo(self, CorpNum, MgtKey):
        """ 상태/요약 정보 조회
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
            return
                문서 상태/요약 정보 object
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httpget('/Cashbill/' + MgtKey, CorpNum)

    def getInfos(self,CorpNum,MgtKeyList):
        """ 상태정보 다량 확인, 최대 1000건
            args
                CorpNum : 회원 사업자 번호
                MgtKeyList : 문서관리번호 목록
            return
                상태정보 목록 as List
            raise
                PopbillException
        """
        if MgtKeyList == None or len(MgtKeyList) < 1:
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
       
        postData = self._stringtify(MgtKeyList)

        return self._httppost('/Cashbill/States',postData,CorpNum)

    def getDetailInfo(self, CorpNum, MgtKey):
        """ 상세정보 조회
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
            return
                문서 상세정보 object
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httpget('/Cashbill/' + MgtKey + '?Detail', CorpNum)

    def sendEmail(self, CorpNum, MgtKey, ReceiverEmail, UserID = None):
        """ 알림메일 재전송
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                ReceiverEmail : 수신자 이메일 주소
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if ReceiverEmail == None or ReceiverEmail == "" :
            raise PopbillException(-99999999,"수신자 메일주소가 입력되지 않았습니다.")   

        postData = self._stringtify({"receiver" : ReceiverEmail})

        return self._httppost('/Cashbill/' + MgtKey, postData, CorpNum, UserID, "EMAIL")

    def sendSMS(self, CorpNum, MgtKey, Sender, Receiver, Contents, UserID = None):
        """ 알림문자 전송
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                Sender : 발신번호
                Receiver : 수신번호
                Contents : 문자 메시지 내용. 최대 90Byte. 초과시 길이가 조정되어 전송됨
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if Receiver == None or Receiver == "" :
            raise PopbillException(-99999999,"문자 수신번호가 입력되지 않았습니다.")

        postData = self._stringtify({
                                    "sender" : Sender,
                                    "receiver" : Receiver, 
                                    "contents" : Contents
                                    })

        return self._httppost('/Cashbill/' + MgtKey, postData, CorpNum, UserID, "SMS")

    def sendFAX(self, CorpNum, MgtKey, Sender, Receiver, UserID = None):
        """ 현금영수증 팩스전송
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                Sender : 발신번호
                Receiver : 수신번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")
        if Receiver == None or Receiver == "" :
            raise PopbillException(-99999999,"팩스 수신번호가 입력되지 않았습니다.")

        postData = self._stringtify({
                                        "sender" : Sender,
                                        "receiver" : Receiver 
                                    })

        return self._httppost('/Cashbill/' + MgtKey, postData, CorpNum, UserID, "FAX")


    def getLogs(self, CorpNum, MgtKey):
        """ 문서이력 조회
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
            return
                문서 이력 목록 as List
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        return self._httpget('/Cashbill/' + MgtKey + '/Logs', CorpNum)

    def getPopUpURL(self, CorpNum, MgtKey, UserID):
        """ 현금영수증 1장의 팝빌 화면을 볼수있는 팝업 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Cashbill/' + MgtKey + '?TG=POPUP', CorpNum, UserID)

        return result.url

    def getPrintURL(self, CorpNum, MgtKey, UserID):
        """ 공급자용 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Cashbill/' + MgtKey + '?TG=PRINT', CorpNum, UserID)    

        return result.url


    def getEPrintURL(self, CorpNum, MgtKey, UserID):
        """ 공급받는자용 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Cashbill/' + MgtKey + '?TG=EPRINT', CorpNum, UserID)   

        return result.url


    def getMailURL(self, CorpNum, MgtKey, UserID):
        """ 공급받는자용 메일 링크 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKey : 문서관리번호
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKey == None or MgtKey == "" :
            raise PopbillException(-99999999,"관리번호가 입력되지 않았습니다.")

        result = self._httpget('/Cashbill/' + MgtKey + '?TG=MAIL', CorpNum, UserID) 

        return result.url


    def getMassPrintURL(self, CorpNum, MgtKeyList, UserID):
        """ 다량 인쇄 URL 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MgtKeyList : 문서관리번호 배열
                UserID : 팝빌회원 아이디
            return
                팝빌 URL as str
            raise 
                PopbillException
        """
        if MgtKeyList == None:
            raise PopbillException(-99999999,"관리번호 배열이 입력되지 않았습니다.")

        postData = self._stringtify(MgtKeyList)

        result = self._httppost('/Cashbill/Prints', postData, CorpNum, UserID)

        return result.url

class Cashbill(object):
    def __init__(self,**kwargs):
        self.__dict__ = kwargs
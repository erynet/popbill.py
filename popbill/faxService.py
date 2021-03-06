# -*- coding: utf-8 -*-
# Module for Popbill FAX API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : Kim Seongjun (pallet027@gmail.com)
# Written : 2015-01-21
# Thanks for your interest. 
from datetime import datetime
from .base import PopbillBase,PopbillException,File

class FaxService(PopbillBase):
    """ 팝빌 팩스 API Service Implementation. """

    def __init__(self, LinkID, SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """
        super(self.__class__,self).__init__(LinkID,SecretKey)
        self._addScope("160")
        
    def getURL(self, CorpNum, UserID, ToGo):
        """ 팩스 관련 팝빌 URL 
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
                TOGO : 팩스관련 기능 지정 문자. (BOX - 전송내역조회)
            return
                30초 보안 토큰을 포함한 url
            raise 
                PopbillException
        """

        result = self._httpget('/FAX/?TG=' + ToGo , CorpNum,UserID)
        return result.url

    def getUnitCost(self,CorpNum):
        """ 팩스 전송 단가 확인
            args
                CorpNum : 팝빌회원 사업자번호
            return
                전송 단가 by float
            raise 
                PopbillException
        """

        result = self._httpget('/FAX/UnitCost' ,CorpNum)
        return int(result.unitCost)


    def getFaxResult(self, CorpNum, ReceiptNum, UserID = None):
        """ 팩스 전송결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 전송요청시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                팩스전송정보 as list 
            raise 
                PopbillException
        """

        return self._httpget('/FAX/' + ReceiptNum, CorpNum, UserID)


    def cancelReserve(self, CorpNum, ReceiptNum, UserID = None):
        """ 팩스 예약전송 취소
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 팩스 전송요청(sendFAX)시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """

        return self._httpget('/FAX/' + ReceiptNum + '/Cancel', CorpNum, UserID)
    

    def sendFax(self, CorpNum, SenderNum, ReceiverNum, ReceiverName, FilePath, ReserveDT = None, UserID = None):
        """ 팩스 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                SenderNum : 발신자 번호 
                ReceiverNum : 수신자 번호
                ReceiverName : 수신자 명 
                FilePath : 발신 파일경로 
                ReserveDT : 예약시간(형식 yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """
        receivers  = []
        receivers.append(FaxReceiver(receiveNum = ReceiverNum,
                                     receiveName = ReceiverName)
                        )

        return self.sendFax_multi(CorpNum, SenderNum, receivers, FilePath, ReserveDT, UserID)

    def sendFax_multi(self, CorpNum, SenderNum, Receiver, FilePath, ReserveDT = None , UserID = None):
        """ 팩스 전송
            args
                CorpNum : 팝빌회원 사업자번호
                SenderNum : 발신자 번호 (동보전송용)
                Receiver : 수신자 번호(동보전송용)
                FilePath : 발신 파일경로 
                ReserveDT : 예약시간(형식 yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        if SenderNum == None or SenderNum == "" :
            raise PopbillException(-99999999,"발신자 번호가 입력되지 않았습니다.")
        if Receiver == None:
            raise PopbillException(-99999999,"수신자 정보가 입력되지 않았습니다.")
        if not (type(Receiver) is str or type(Receiver) is FaxReceiver or type(Receiver) is list) :
            raise PopbillException(-99999999,"'Receiver' argument type error. 'FaxReceiver' or List of 'FaxReceiver'.")
        if FilePath == None :
            raise PopbillException(-99999999,"발신 파일경로가 입력되지 않았습니다.")
        if not (type(FilePath) is str or type(FilePath) is list) :
            raise PopbillException(-99999999,"발신 파일은 파일경로 또는 경로목록만 입력 가능합니다.")
        if type(FilePath) is list and (len(FilePath) < 1 or len(FilePath) > 5) :
            raise PopbillException(-99999999,"파일은 1개 이상, 5개 까지 전송 가능합니다.")

        req = {"snd" : SenderNum , "fCnt": 1 if type(FilePath) is str else len(FilePath) , "rcvs" : [] , "sndDT" : None}

        if(type(Receiver) is str):        
            Receiver = FaxReceiver(receiveNum=Receiver)
            
        if(type(Receiver) is FaxReceiver):
            Receiver = [Receiver]

        for r in Receiver:
            req['rcvs'].append({"rcv" : r.receiveNum, "rcvnm" : r.receiveName})

        if ReserveDT != None :
            req['sndDT'] = ReserveDT

        postData = self._stringtify(req)

        if(type(FilePath) is str):
            FilePath = [FilePath]
        
        files = []

        for filePath in FilePath:
            with open(filePath,"rb") as f:
                files.append(File(fieldName='file',
                              fileName=f.name,
                              fileData=f.read())
                            )
                
        result = self._httppost_files('/FAX',postData,files,CorpNum,UserID)

        return result.receiptNum


class FaxReceiver(object):
    def __init__(self,**kwargs):
        self.__dict__ = dict.fromkeys(['receiveNum','receiveName'])
        self.__dict__.update(kwargs)
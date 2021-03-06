# -*- coding: utf-8 -*-
# Module for Popbill Message API. It include base functionality of the
# RESTful web service request and parse json result. It uses Linkhub module
# to accomplish authentication APIs.
#
# http://www.popbill.com
# Author : John Yohan (yhjeong@linkhub.co.kr)
# Written : 2015-03-20
# Thanks for your interest.
from .base import PopbillBase,PopbillException,File

class MessageService(PopbillBase):
    """ 팝빌 문자 API Service Implementation. """
    
    def __init__(self,LinkID,SecretKey):
        """생성자
            args
                LinkID : 링크허브에서 발급받은 링크아이디(LinkID)
                SecretKeye 링크허브에서 발급받은 비밀키(SecretKey)
        """
        super(self.__class__, self).__init__(LinkID,SecretKey)
        self._addScope("150")
        self._addScope("151")
        self._addScope("152")

    def getUnitCost(self, CorpNum, MsgType):
        """ 문자 전송 단가 확인
            args
                CorpNum : 팝빌회원 사업자번호
                MsgType : 문자 유형(SMS, LMS)
            return
                전송 단가 by float
            raise 
                PopbillException
        """
        if MsgType == None or MsgType == "" :
            raise PopbillException(-99999999,"전송유형이 입력되지 않았습니다.")

        result = self._httpget('/Message/UnitCost?Type=' + MsgType, CorpNum)
        return float(result.unitCost)

    def sendSMS(self, CorpNum, Sender, Receiver, ReceiverName, Contents, reserveDT, UserID = None):
        """ 단문 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호 
                Receiver : 수신번호
                ReceiverName : 수신자명
                Contents : 메시지 내용(90Byte 초과시 길이가 조정되어 전송됨)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """
        Messages = []
        Messages.append(MessageReceiver(
                                    snd = Sender,
                                    rcv = Receiver,
                                    rcvnm = ReceiverName,
                                    msg = Contents)
                        )

        return self.sendMessage("SMS", CorpNum, Sender, '', Contents, Messages, reserveDT, UserID)


    def sendSMS_multi(self, CorpNum, Sender, Contents, Messages, reserveDT, UserID = None):
        """ 단문 문자메시지 다량전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Contents : 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        return self.sendMessage("SMS", CorpNum, Sender, '', Contents, Messages, reserveDT, UserID)

    def sendLMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, reserveDT, UserID = None):
        """ 장문 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호 
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(2000Byte 초과시 길이가 조정되어 전송됨)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        Messages = []
        Messages.append(MessageReceiver(
                                    snd = Sender,
                                    rcv = Receiver,
                                    rcvnm = ReceiverName,
                                    msg = Contents,
                                    sjt= Subject)
                        )

        return self.sendMessage("LMS", CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID)

    def sendLMS_multi(self, CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID = None):
        """ 장문 문자메시지 다량전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        return self.sendMessage("LMS", CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID)

    def sendMMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, filePath, reserveDT, UserID = None):
        """ 멀티 문자메시지 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호 
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(2000Byte 초과시 길이가 조정되어 전송됨)
                filePath : 전송하고자 하는 파일 경로
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """
        Messages = []
        Messages.append(MessageReceiver(
                                    snd = Sender,
                                    rcv = Receiver,
                                    rcvnm = ReceiverName,
                                    msg = Contents,
                                    sjt= Subject)
                        )

        return self.sendMMS_Multi(CorpNum, Sender, Subject, Contents, Messages, filePath, reserveDT, UserID)

    def sendMMS_Multi(self, CorpNum, Sender, Subject, Contents, Messages, FilePath, reserveDT, UserID = None):
        """ 멀티 문자메시지 다량 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                FilePath : 전송하고자 하는 파일 경로
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """
        if Messages == None or len(Messages) < 1 :
            raise PopbillException(-99999999,"전송할 메시지가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != '':
            req['snd'] = Sender
        if Contents != None or Contents != '':
            req['content'] = Contents
        if Subject != None or Subject != '':
            req['subject'] = Subject
        if reserveDT != None or reserveDT != '':
            req['sndDT'] = reserveDT
        if Messages != None or Messages != '':
            req['msgs'] = Messages

        postData = self._stringtify(req)

        files = []
        try:
            with open(FilePath,"rb") as F:
                files = [File(fieldName='file',
                              fileName=F.name,
                              fileData=F.read())]
        except IOError :
            raise PopbillException(-99999999,"해당경로에 파일이 없거나 읽을 수 없습니다.")

        result =  self._httppost_files('/MMS', postData, files, CorpNum, UserID)

        return result.receiptNum



    def sendXMS(self, CorpNum, Sender, Receiver, ReceiverName, Subject, Contents, reserveDT, UserID = None):
        """ 단/장문 자동인식 단건 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신번호 
                Receiver : 수신번호
                ReceiverName : 수신자명
                Subject : 메시지 제목
                Contents : 메시지 내용(90Byte를 기준으로 문자유형이 자동인식 되어 전송)
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        Messages = []
        Messages.append(MessageReceiver(
                                    snd = Sender,
                                    rcv = Receiver,
                                    rcvnm = ReceiverName,
                                    msg = Contents,
                                    sjt= Subject)
                        )

        return self.sendMessage("XMS", CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID)

    def sendXMS_multi(self, CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID = None):
        """ 단/장문 자동인식 다량 전송
            args
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """

        return self.sendMessage("XMS", CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID)

    def sendMessage(self, MsgType, CorpNum, Sender, Subject, Contents, Messages, reserveDT, UserID = None):
        """ 문자 메시지 전송
            args
                MsgType : 문자 전송 유형(단문:SMS, 장문:LMS, 단/장문:XMS)
                CorpNum : 팝빌회원 사업자번호
                Sender : 발신자번호 (동보전송용)
                Subject : 장문 메시지 제목 (동보전송용)
                Contents : 장문 문자 내용 (동보전송용)
                Messages : 개별전송정보 배열
                reserveDT : 예약전송시간 (형식. yyyyMMddHHmmss)
                UserID : 팝빌회원 아이디
            return
                접수번호 (receiptNum)
            raise 
                PopbillException
        """
        if Messages == None or len(Messages) < 1 :
            raise PopbillException(-99999999,"전송할 메시지가 입력되지 않았습니다.")

        req = {}

        if Sender != None or Sender != '':
            req['snd'] = Sender
        if Contents != None or Contents != '':
            req['content'] = Contents
        if Subject != None or Subject != '':
            req['subject'] = Subject
        if reserveDT != None or reserveDT != '':
            req['sndDT'] = reserveDT
        if Messages != None or Messages != '':
            req['msgs'] = Messages

        postData = self._stringtify(req)

        result =  self._httppost('/' + MsgType, postData, CorpNum, UserID)

        return result.receiptNum

    def getMessages(self, CorpNum, ReceiptNum, UserID = None):
        """ 문자 전송결과 조회
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 전송요청시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                전송정보 as list 
            raise 
                PopbillException
        """
        if ReceiptNum == None or ReceiptNum == '' :
            raise PopbillException(-99999999,"접수번호가 입력되지 않았습니다.")

        return self._httpget('/Message/' + ReceiptNum, CorpNum)

    def cancelReserve(self, CorpNum, ReceiptNum, UserID = None):
        """ 문자 예약전송 취소
            args
                CorpNum : 팝빌회원 사업자번호
                ReceiptNum : 전송요청시 발급받은 접수번호
                UserID : 팝빌회원 아이디
            return
                처리결과. consist of code and message
            raise 
                PopbillException
        """
        if ReceiptNum == None or ReceiptNum == '' :
            raise PopbillException(-99999999,"접수번호가 입력되지 않았습니다.")

        return self._httpget('/Message/' + ReceiptNum + '/Cancel', CorpNum)


    def getURL(self, CorpNum, UserID, TOGO):
        """ 문자 관련 팝빌 URL 
            args
                CorpNum : 팝빌회원 사업자번호
                UserID : 팝빌회원 아이디
                TOGO : BOX (전송내역조회 팝업)
            return
                팝빌 URL
            raise 
                PopbillException
        """

        result = self._httpget('/Message/?TG=' + TOGO, CorpNum, UserID)
        
        return result.url

class MessageReceiver(object):
    def __init__(self,**kwargs):
        self.__dict__ = dict.fromkeys(['snd','rcv','rcvnm','msg','sjt'])
        self.__dict__.update(kwargs)
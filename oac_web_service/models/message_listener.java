package oac.jms.listener;  
  
import javax.jms.JMSException;  
import javax.jms.Message;  
import javax.jms.MessageListener;  
import javax.jms.TextMessage;  
  
import org.apache.log4j.Logger;  
  
public class MessageListenerImpl implements MessageListener  
{  
 private static final Logger LOG = Logger.getLogger(MessageListenerImpl.class);  
  
 public void onMessage(Message message)  
 {  
  if ((message instanceof TextMessage))  
  {  
   try  
   {  
    LOG.info("RECEIVED: MESSAGE ID: " + message.getJMSMessageID());  
    LOG.info("RECEIVED: MESSAGE TEXT: " + ((TextMessage) message).getText());  
   }  
   catch (JMSException e)  
   {  
    e.printStackTrace();  
   }  
  }  
 }  
}
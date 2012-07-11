#!/bin/bash
sudo /etc/init.d/tomcat6 stop
#sudo /etc/init.d/tomcat7 stop

sleep 6

sudo rm -rf /var/www/tomcat/apache-tomcat-6.0.35/webapps/oac_web_service*
sudo rm -rf /var/www/tomcat/apache-tomcat-7.0.27/webapps/oac_web_service*

/usr/java/jdk1.6.0_32/bin/javac amq/MessageListenerImpl.java
jar cvf MessageListenerImpl.jar amq/MessageListenerImpl.class
mv MessageListenerImpl.jar WEB-INF/lib/
rm amq/MessageListenerImpl.class

jar cvf oac_web_service.war WEB-INF oac_web_service.py oac_web_service README
sudo cp oac_web_service.war /var/www/tomcat/apache-tomcat-6.0.35/webapps/
sudo cp oac_web_service.war /var/www/tomcat/apache-tomcat-7.0.27/webapps/

sudo /etc/init.d/tomcat6 start
#sudo /etc/init.d/tomcat7 start

sleep 6

sudo touch /var/www/tomcat/apache-tomcat-6.0.35/webapps/fedora/WEB-INF/web.xml

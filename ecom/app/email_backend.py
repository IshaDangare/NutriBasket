"""Custom email backend that bypasses SSL certificate verification."""

import ssl
import smtplib
from django.core.mail.backends.smtp import EmailBackend as SMTPEmailBackend


class SSLInsecureEmailBackend(SMTPEmailBackend):
    """SMTP backend that bypasses SSL certificate verification.
    
    Use this only for development! Never use in production.
    """
    
    def open(self):
        """Connect to the SMTP server using unverified SSL context."""
        if self.connection is not None:
            return False
        
        try:
            # Create SMTP connection
            self.connection = smtplib.SMTP(self.host, self.port, timeout=self.timeout)
            
            # Identify ourselves to SMTP
            self.connection.ehlo()
            
            # If TLS is enabled, upgrade the connection
            if self.use_tls:
                # Use unverified context to bypass SSL certificate verification
                context = ssl._create_unverified_context()
                self.connection.starttls(context=context)
                self.connection.ehlo()
            
            # Authenticate
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            
            return True
        except Exception as e:
            if not self.fail_silently:
                raise


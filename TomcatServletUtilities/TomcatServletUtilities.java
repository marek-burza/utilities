import java.io.IOException;
import java.io.InputStream;
import java.io.PrintWriter;
import java.io.StringWriter;
import java.io.UnsupportedEncodingException;

import java.net.URI;
import java.net.URLEncoder;

import java.security.SecureRandom;
import java.security.cert.X509Certificate;

import java.text.DateFormat;
import java.text.SimpleDateFormat;

import java.util.Date;
import java.util.Enumeration;

import java.net.URL;
import java.net.URLConnection;
import java.net.URLEncoder;

import javax.net.ssl.HostnameVerifier;
import javax.net.ssl.HttpsURLConnection;
import javax.net.ssl.SSLContext;
import javax.net.ssl.SSLSession;
import javax.net.ssl.TrustManager;
import javax.net.ssl.X509TrustManager;
import javax.servlet.ServletContext;
import javax.servlet.http.Cookie;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class TomcatServletUtilities {
  public static void encodeURLArgument(String argument) throws UnsupportedEncodingException {
    return URLEncoder.encode(argument, "UTF-8");
  }
  
  public static void redirectRequest(HttpServletResponse response, String redirect) {
    response.setStatus(response.SC_MOVED_TEMPORARILY);
    response.setHeader("Location", redirect);
  }

  public static void forwardHeader(String header, HttpServletRequest request, HttpServletResponse response) {
    String value = request.getHeader(header);
    response.setHeader(header, value);
  }
  
  public static void setCookie(String name, String value, String domain /* .example.com */, String path /* / */, HttpServletResponse response) {
    Cookie cookie = new Cookie(name, value);
    cookie.setDomain(domain);
    cookie.setPath(path);
    response.addCookie(cookie);
  }

  public static void printHeaders(HttpServletRequest request) {
    System.out.println("--- HEADERS ---");
    Enumeration<String> headers = request.getHeaderNames();
    while (headers.hasMoreElements()) {
      String header = headers.nextElement();
      System.out.println(header + ": " + request.getHeader(header));
    }
  }

  public static void printCookies(HttpServletRequest request) {
    System.out.println("--- COOKIES ---");
    for (Cookie cookie : request.getCookies()) {
      System.out.println(cookie.getName() + ": " + cookie.getValue());
    }
  }
  
  private static TrustManager[] gullibleMAnager = new TrustManager[] {
    new X509TrustManager() {
      public X509Certificate[] getAcceptedIssuers() {
        return null;
      }
      public void checkClientTrusted(X509Certificate[] certs, String authType) {
      }
      public void checkServerTrusted(X509Certificate[] certs, String authType) {
      }
    }
  };

  public static void trustEveryone() {
    try {
      SSLContext context = SSLContext.getInstance("SSL");
      context.init(null, gullibleManager, new SecureRandom());
      HttpsURLConnection.setDefaultSSLSocketFactory(context.getSocketFactory());
    } catch (Exception exception) {
    }
    HttpsURLConnection.setDefaultHostnameVerifier(
      new HostnameVerifier() {
        public boolean verify(String hostname, SSLSession session) {
          return true;
        }
      }
    );
  }
  
  // The property can be a header of a cookie, e.g.:
  // property = "Cookie"; value = "OREO=\"" + content + "\";";
  public static String callURL(String url; String property, String value) {
    try {
      URLConnection connection = new URL(url).openConnection();
      connection.setRequestProperty(property, value);
      connection.setDoOutput(false);
      connection.setDoInput(true);
      connection.connect();
      InputStream stream = connection.getInputStream();
      StringBuilder builder = new StringBuilder();
      int octet;
      while ((octet = stream.read()) != -1) {
        builder.append((char) octet);
      }
      return builder.toString();
    } catch (IOException exception) {
      return exception2String(exception);
    }
  }

  public static String exception2String(Throwable exception){
    StringWriter writer = new StringWriter();
    exception.printStackTrace(new PrintWriter(writer));
    return writer.toString();
  }
  
  // JAVA_OPTS=-DPROPERTY=VALUE
  // getSystemProperty("PROPERTY") --> "VALUE"
  public static void getSystemProperty(String property){
    return System.getProperty("OTHER_URL");
  }
}
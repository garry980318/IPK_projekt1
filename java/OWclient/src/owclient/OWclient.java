/**
 * @author Radoslav Grencik <xgrenc00@stud.fit.vutbr.cz>
 */
package owclient;

import java.io.IOException;
import java.io.InputStream;
import java.io.OutputStream;
import java.io.PrintWriter;
import java.net.Socket;
import java.util.Scanner;

/**
 *
 */
public class OWclient {

    private static String host, resource;
    private static final int PORT = 80;
    private static Socket s;

    public static void get() {
        try {
            InputStream input = s.getInputStream();
            OutputStream output = s.getOutputStream();
            try (Scanner sc = new Scanner(input)) {
                PrintWriter pw = new PrintWriter(output);

                String command = "GET " + resource + " HTTP/1.1\n" + "Host: " + host + "\n\n";
                pw.print(command);
                pw.flush();

                String l = "";
                for (int i = 0; i < 12; i++) {
                    l = sc.nextLine();
                }

                char[] arr = l.toCharArray();

                int i = 0, brac = 0;
                while (i < arr.length) {
                    if (arr[i] == '{') {
                        brac++;
                    }
                    if (arr[i] == '}') {
                        brac--;
                    }
                    if (arr[i] == '{' || arr[i] == '}' || arr[i] == '"' || arr[i] == '[' || arr[i] == ']') {
                        arr[i] = 0;
                    }

                    if (arr[i] == ',' && brac == 1) {
                        arr[i] = '\n';
                    }
                    System.out.printf("%c", arr[i]);
                    i++;
                }

                i = 0;
                int counter = 0;
                while (i < arr.length) {
                    if (arr[i] == '\n') counter++;
                    if (counter == 10) {
                        i = i + 9;
                        break;
                    }
                    i++;
                }

                char[] cityarr = new char[50];
                counter = 0;
                while (arr[i] != '\n') {
                    cityarr[counter] = arr[i];
                    System.out.printf("%c", cityarr[counter]);
                    i++;
                    counter++;
                }

                s.close();
            }
        } catch (IOException e) {
            System.err.println("Problem: " + e.getMessage());
        }
    }

    /**
     * @param args the command line arguments
     */
    public static void main(String[] args) {
        try {
            String loc = "Prague";
            String appid = "b48908b86c2a129e60b2f84c8a1c8d67";
            host = "api.openweathermap.org";
            resource = "/data/2.5/weather?q=" + loc + "&APPID=" + appid +"&units=metric";
            s = new Socket(host, PORT);

            get();
        } catch (IOException e) {
            System.err.println("Problem: " + e.getMessage());
        }
    }

}

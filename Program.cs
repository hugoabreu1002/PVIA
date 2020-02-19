using System;
using System.Windows.Forms;
using System.Drawing;
using System.IO;
using System.Net;
using Newtonsoft.Json.Linq;
using System.Threading;
using System.Diagnostics;

namespace Plataforma_Integrada
{
    public class Program
    {

        [STAThread]
        static void Main()
        {
            Application.EnableVisualStyles();
            Application.SetCompatibleTextRenderingDefault(false);
            Application.Run(new Form1());
        }

        public static Image Request_time_serie(string nome_usina)
        {
            // Construct HTTP request to get the file
            string uirWebAPI;
            Image img;

            uirWebAPI = "http://localhost:8080/time_series";

            Uri uri = new Uri(uirWebAPI);
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.ContentType = "application/json";
            request.Method = "POST";

            using (var streamWriter = new StreamWriter(request.GetRequestStream()))
            {
                string json = "{\"Usina\":\"" + nome_usina + "\"}";
                streamWriter.Write(json);
            }

            using (WebResponse response = request.GetResponse())
            {
                using (Stream responseStream = response.GetResponseStream())
                {
                    img = Image.FromStream(responseStream);
                }
            }

            return img;
        }

        public static string[] Request_Nordest_columns()
        {
            string uirWebAPI, webResponse;

            uirWebAPI = "http://localhost:8080/Nordeste_columns";

            Uri uri = new Uri(uirWebAPI);
            WebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.ContentType = "application/json";
            request.Method = "POST";
            HttpWebResponse response = (HttpWebResponse)request.GetResponse();
            using (StreamReader streamReader = new StreamReader(response.GetResponseStream()))
            {
                webResponse = streamReader.ReadToEnd();
            }

            JObject jObject = JObject.Parse(webResponse);
            string displayName = (string)jObject.SelectToken("lista_colunas").ToString();
            string[] strlist = displayName.Substring(1, displayName.Length - 2).Replace(" ", "").Replace("\r", "").Replace("\n", "").Replace("\"", "").Split(',');//get_list_strings(displayName.Substring(1, displayName.Length - 2));                                                                                

            return strlist;
        }

        public static Image Request_Nordest_column_plot(string column, string colormap)
        {
            string uirWebAPI;
            Image img;

            uirWebAPI = "http://localhost:8080/Plot_Nordeste";

            Uri uri = new Uri(uirWebAPI);
            WebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.Method = "POST";
            request.ContentType = "application/json";

            using (var streamWriter = new StreamWriter(request.GetRequestStream()))
            {
                string json = "{\"Coluna\":\""+column+"\", \"ColorMap\":\""+colormap+"\"}";
                streamWriter.Write(json);
            }

            using (WebResponse response = request.GetResponse())
            {
                using (Stream responseStream = response.GetResponseStream())
                {
                    img = Image.FromStream(responseStream);
                }
            }

            return img;
        }
        public static string Request_Nordest_column_plotly(string column, string colormap)
        {

            string uirWebAPI, webResponse;

            uirWebAPI = "http://localhost:8080/Plotly_Nordeste";

            Uri uri = new Uri(uirWebAPI);
            WebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.Method = "POST";
            request.ContentType = "application/json";

            using (var streamWriter = new StreamWriter(request.GetRequestStream()))
            {
                string json = "{\"Coluna\":\"" + column + "\", \"ColorMap\":\"" + colormap + "\"}";
                streamWriter.Write(json);
            }

            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            using (StreamReader streamReader = new StreamReader(response.GetResponseStream()))
            {
                webResponse = streamReader.ReadToEnd();
            }

            return webResponse;
        }

        public static string Request_INMET_Scraping(string nome_usuario, string senha_usuario)
        {
            // Construct HTTP request to get the file
            string uirWebAPI, webResponse;

            uirWebAPI = "http://localhost:8080/inmet_scraping";

            Uri uri = new Uri(uirWebAPI);
            HttpWebRequest request = (HttpWebRequest)WebRequest.Create(uri);
            request.ContentType = "application/json";
            request.Method = "POST";

            using (var streamWriter = new StreamWriter(request.GetRequestStream()))
            {
                string json = "{\"login\":\"" + nome_usuario + "\", \"senha\": \"" +senha_usuario+"\"}";
                streamWriter.Write(json);
            }

            HttpWebResponse response = (HttpWebResponse)request.GetResponse();

            using (StreamReader streamReader = new StreamReader(response.GetResponseStream()))
            {
                webResponse = streamReader.ReadToEnd();
            }

            return webResponse;
        }

        public static void StartServer()
        {

            Process cmd = new Process();

            cmd.StartInfo.FileName = "cmd.exe";
            cmd.StartInfo.RedirectStandardInput = true;
            cmd.StartInfo.RedirectStandardOutput = true;
            cmd.StartInfo.CreateNoWindow = true;
            cmd.StartInfo.UseShellExecute = false;
            cmd.Start();

            cmd.StandardInput.WriteLine("cd ..");
            cmd.StandardInput.WriteLine("cd ..");
            cmd.StandardInput.WriteLine("cd python");
            cmd.StandardInput.WriteLine("python flask_server.py");

            cmd.WaitForExit();
            Console.WriteLine(cmd.StandardOutput.ReadToEnd());

            Thread.Sleep(100);
        }

    }

}
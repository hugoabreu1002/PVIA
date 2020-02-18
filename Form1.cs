using System;
using System.Drawing;
using System.IO;
using System.Windows.Forms;
using CefSharp;
using CefSharp.WinForms;
using System.Diagnostics;
using System.Threading;

namespace Plataforma_Integrada
{
    public partial class Form1 : Form
    {
        public ChromiumWebBrowser chromeBrowser;
        public string exePath = Application.StartupPath;
        FormWindowState LastWindowState = FormWindowState.Minimized;

        public Form1()
        {
            InitializeComponent();
            InitializeChromium();
        }

        private void InitializeChromium()
        {
            CefSettings settings = new CefSettings();
            // Initialize cef with the provided settings
            Cef.Initialize(settings);
            // Create a browser component
            this.chromeBrowser = new ChromiumWebBrowser("");
            // Add it to the form and fill it to the form window.
            this.panel3.Controls.Add(this.chromeBrowser);
        }

        private void Button3_Click(object sender, EventArgs e)
        {
            Image img;
            string usina = listBox1.SelectedItem.ToString();
            img = Program.Request_time_serie(usina);
            pictureBox1.Image = img;
            pictureBox1.SizeMode = PictureBoxSizeMode.StretchImage;
        }

        private void Button1_Click(object sender, EventArgs e)
        {
            Bitmap img;
            string coluna, colormap;
            coluna = "";
            colormap = "";
            try { 
            coluna = listBox2.SelectedItem.ToString();
            colormap = listBox3.SelectedItem.ToString();
            }
            catch
            {
                MessageBox.Show(
                "Escolha uma Coluna e um ColorMap",
                "Error",
                MessageBoxButtons.OK,
                MessageBoxIcon.Warning //For triangle Warning 
                );
            }

            img = new Bitmap (Program.Request_Nordest_column_plot(coluna, colormap));

            double startWidth = img.Width * 0.05;
            double startHeigh = img.Height * 0.10;

            double newWidth = img.Width * 0.90;
            double newHeight = img.Height * 0.85;

            Rectangle cropArea = new Rectangle((int)startWidth, (int)startHeigh, (int)newWidth, (int)newHeight);
            img = img.Clone(cropArea, img.PixelFormat);

            pictureBox2.Image = img;
            pictureBox2.SizeMode = PictureBoxSizeMode.StretchImage;

            string plotlyServiceReturn;
            plotlyServiceReturn = Program.Request_Nordest_column_plotly(coluna, colormap);

            chromeBrowser.Load(exePath.Substring(0, exePath.IndexOf("\\bin")) + "\\python\\plotly_hmtls\\" + coluna + ".html");
        }

        private void Form1_Load(object sender, EventArgs e)
        {
            dateTimePicker1.Format = DateTimePickerFormat.Custom;
            dateTimePicker1.CustomFormat = "dd-MM-yyyy";

            dateTimePicker2.Format = DateTimePickerFormat.Custom;
            dateTimePicker2.CustomFormat = "dd-MM-yyyy";

            textBox1.Text = exePath;
        }

        private void Form1_FormClosing(object sender, FormClosingEventArgs e)
        {
            Cef.Shutdown();
            try { 
                Process cmd = new Process();
                cmd.Kill();
            }
            catch { }
        }

        private void button4_Click(object sender, EventArgs e)
        {

            Thread ServerThread = new Thread(Program.StartServer);

            ServerThread.Start();

            try
            {
                listBox2.Items.Clear();
                listBox2.Items.AddRange(Program.Request_Nordest_columns());
            }
            catch
            {

                MessageBox.Show(
                  "Não é possível conectar ao servidor",
                  "Error",
                  MessageBoxButtons.OK,
                  MessageBoxIcon.Stop //For triangle Warning 
                );
            }

            listBox3.Items.Clear();
            string[] strlist = { "Reds", "Greens", "Blues", "Jet", "Greys", "Viridis", "Cividis", "Magma", "Plasma", "Wistia" };
            listBox3.Items.AddRange(strlist);
        }

        private void button2_Click(object sender, EventArgs e)
        {
            using (var fbd = new FolderBrowserDialog())
            {
                DialogResult result = fbd.ShowDialog();

                if (result == DialogResult.OK && !string.IsNullOrWhiteSpace(fbd.SelectedPath))
                {
                    exePath = fbd.SelectedPath;
                    textBox1.Text = exePath;
                    string[] files = Directory.GetFiles(fbd.SelectedPath);
                }
            }
        }
    }
}

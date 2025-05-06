using System;
using System.Windows.Forms;
using FixClientService.Sessions;

namespace MyWinFormsApp
{
    public class Form1 : Form
    {
        private InitializeFixClient FixInstance;
        private Form2 _form2;
        private TextBox txtSymbol, txtPrice, txtQuantity;
        private ComboBox cmbOrderType, cmbSide;
        private Button btnSend;

        public Form1(InitializeFixClient fixInstance, Form2 form2)
        {
            FixInstance = fixInstance;
            _form2 = form2;
            InitializeForm();
        }

        private void InitializeForm()
        {
            // **Form Settings**
            this.Text = "Order Entry Form";
            this.Size = new System.Drawing.Size(400, 300);

            // **Label and TextBox for Symbol**
            Label lblSymbol = new Label { Text = "Symbol:", Location = new System.Drawing.Point(20, 20) };
            txtSymbol = new TextBox { Location = new System.Drawing.Point(120, 20), Width = 200 };

            // **Label and TextBox for Price**
            Label lblPrice = new Label { Text = "Price:", Location = new System.Drawing.Point(20, 60) };
            txtPrice = new TextBox { Location = new System.Drawing.Point(120, 60), Width = 200 };

            // **Label and TextBox for Quantity**
            Label lblQuantity = new Label { Text = "Quantity:", Location = new System.Drawing.Point(20, 100) };
            txtQuantity = new TextBox { Location = new System.Drawing.Point(120, 100), Width = 200 };

            // **Label and ComboBox for Order Type**
            Label lblOrderType = new Label { Text = "Order Type:", Location = new System.Drawing.Point(20, 140) };
            cmbOrderType = new ComboBox
            {
                Location = new System.Drawing.Point(120, 140),
                Width = 200,
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbOrderType.Items.AddRange(new object[] { "MKT", "LMT" });

            // **Label and ComboBox for Side (Buy/Sell)**
            Label lblSide = new Label { Text = "Side:", Location = new System.Drawing.Point(20, 180) };
            cmbSide = new ComboBox
            {
                Location = new System.Drawing.Point(120, 180),
                Width = 200,
                DropDownStyle = ComboBoxStyle.DropDownList
            };
            cmbSide.Items.AddRange(new object[] { "BUY", "SELL" });

            // **Send Button**
            btnSend = new Button
            {
                Text = "Send Order",
                Location = new System.Drawing.Point(120, 220),
                Size = new System.Drawing.Size(100, 30)
            };
            btnSend.Click += Button_Click;

            // **Add Controls to Form**
            this.Controls.Add(lblSymbol);
            this.Controls.Add(txtSymbol);
            this.Controls.Add(lblPrice);
            this.Controls.Add(txtPrice);
            this.Controls.Add(lblQuantity);
            this.Controls.Add(txtQuantity);
            this.Controls.Add(lblOrderType);
            this.Controls.Add(cmbOrderType);
            this.Controls.Add(lblSide);
            this.Controls.Add(cmbSide);
            this.Controls.Add(btnSend);
        }

        private void Button_Click(object sender, EventArgs e)
        {
            // Validate input
            if (string.IsNullOrWhiteSpace(txtSymbol.Text) ||
                string.IsNullOrWhiteSpace(txtPrice.Text) ||
                string.IsNullOrWhiteSpace(txtQuantity.Text) ||
                cmbOrderType.SelectedItem == null ||
                cmbSide.SelectedItem == null)
            {
                MessageBox.Show("Please fill in all fields", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            // Convert inputs
            string symbol = txtSymbol.Text;
            if (!decimal.TryParse(txtPrice.Text, out decimal price) || price <= 0)
            {
                MessageBox.Show("Invalid price", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (!int.TryParse(txtQuantity.Text, out int quantity) || quantity <= 0)
            {
                MessageBox.Show("Invalid quantity", "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }

            string orderType = cmbOrderType.SelectedItem.ToString();
            string side = cmbSide.SelectedItem.ToString();

            // Send the order
            FixInstance.SendMessage(symbol, orderType, quantity, side, price);
            _form2.AddOrder(Guid.NewGuid().ToString(), orderType, symbol, quantity, side, price);
            // MessageBox.Show($"Order sent: {side} {quantity} {symbol} @ {price}", "Success", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }
    }
}

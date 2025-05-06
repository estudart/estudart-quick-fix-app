
namespace MyWinFormsApp
{
    public partial class Form2 : Form
    {
        private List<string[]> _orders = new List<string[]>(); // List to store orders
        private DataGridView _dataGridView1 = new DataGridView { ColumnCount = 6, Dock = DockStyle.Fill };

        public Form2()
        {
            InitializeComponent();
            InitializeTable();
        }

        public void InitializeTable()
        {
            this.Text = "Orders";
            this.Size = new Size(930, 450);

            _dataGridView1.Columns[0].Name = "Order ID";
            _dataGridView1.Columns[1].Name = "OrderType";
            _dataGridView1.Columns[2].Name = "Symbol";
            _dataGridView1.Columns[3].Name = "Quantity";
            _dataGridView1.Columns[4].Name = "Side";
            _dataGridView1.Columns[5].Name = "Price";

            Controls.Add(_dataGridView1); // Add DataGridView to the form
        }

        public void AddOrder(
            string orderId, 
            string orderType,
            string symbol,
            int quantity,
            string side,
            decimal price)
        {
            _orders.Add(new string[] { 
                orderId, 
                orderType, 
                symbol,
                quantity.ToString(),
                side,
                price.ToString()
            });

            // Add new row
            _dataGridView1.Rows.Add(
                orderId, 
                orderType, 
                symbol, 
                quantity, 
                side, 
                price
            ); 
        }
    }
}


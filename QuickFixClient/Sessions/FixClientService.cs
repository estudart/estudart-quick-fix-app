using QuickFix;
using QuickFix.Transport;
using QuickFix.Logger;
using QuickFix.Store;
using QuickFix.Fields;
using QuickFixClient.Utils;

namespace FixClientService.Sessions
{
    public class InitializeFixClient
    {
        public FixClientSession _fixClientSession;
        private readonly SocketInitiator _initiator;

        public InitializeFixClient()
        {
            // Initialize the FIX application
            _fixClientSession = new FixClientSession();

            // Load FIX session settings from the configuration file
            var settings = new SessionSettings(ConfigProcessor.ProcessConfig("C:\\Users\\erico.studart_hashde\\Desktop\\Personal_projects\\QuickFixApp\\QuickFixClient\\Utils\\config.cfg"));

            // Initialize the required factories
            var storeFactory = new FileStoreFactory(settings);
            var logFactory = new ScreenLogFactory(settings);

            // Create the FIX initiator
            _initiator = new SocketInitiator(_fixClientSession, storeFactory, settings, logFactory);
        }

        public void StartFixSession()
        {
            _initiator.Start();
            Console.WriteLine("FIX Client Started. Press Ctrl+C to quit...");
        }

        public void StopFixSession()
        {
            _initiator.Stop();
            Console.WriteLine("FIX Client Stopped.");
        }

        public void SendMessage(
            string symbol,
            string orderType,
            decimal quantity,
            string side,
            decimal price = 0m
            )
        {
            if (side.ToUpper() == "BUY")
            {
                _fixClientSession.SendMessage(
                    symbol,
                    orderType,
                    quantity,
                    Side.BUY,
                    price
                );
            }
            else if (side.ToUpper() == "SELL")
            {
                _fixClientSession.SendMessage(
                    symbol,
                    orderType,
                    quantity,
                    Side.SELL,
                    price
                );
            }
        }

    }
}

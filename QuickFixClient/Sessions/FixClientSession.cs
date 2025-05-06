using QuickFixClient.Extensions;
using QuickFix;
using QuickFix.Fields;

namespace FixClientService.Sessions
{
    // Implement the FixApplication class which implements the IApplication interface
    public class FixClientSession : IApplication
    {
        private static SessionID? _sessionID;

        public void FromAdmin(QuickFix.Message message, SessionID sessionId)
        {
            Console.WriteLine($"[FromAdmin] Initiator - Session: {sessionId}, Message: {message.ReadableString()}");
        }

        public void FromApp(QuickFix.Message message, SessionID sessionId)
        {
            Console.WriteLine($"[FromApp] Initiator - Session: {sessionId}, Message: {message.ReadableString()}");
        }

        public void OnCreate(SessionID sessionId)
        {
            _sessionID = sessionId;
            Console.WriteLine($"Session has been created: {sessionId}");
        }

        public void OnLogon(SessionID sessionId)
        {
            Console.WriteLine($"[OnLogon] Initiator - Session: {sessionId}");
        }

        public void OnLogout(SessionID sessionId)
        {
            Console.WriteLine($"Logged out: {sessionId}");
        }

        public void ToAdmin(QuickFix.Message message, SessionID sessionId)
        {
            if (message.Header.GetString(Tags.MsgType) == "A")
            {
                Console.WriteLine($"[ToAdmin] Initiator - Session: {sessionId}, Message: {message.ReadableString()}");
            }
            // Log heartbeats sent to the counterparty
            else if (message.Header.GetString(Tags.MsgType) == "0") // Heartbeat
            {
                Console.WriteLine($"[HeartBeat - Initiator] : {sessionId}, Message: {message.ReadableString()}");
            }
        }

        public void ToApp(QuickFix.Message message, SessionID sessionId)
        {
            Console.WriteLine($"[ToApp] Initiator - Session: {sessionId}, Message: {message.ReadableString()}");
        }

        public void SendMessage(
            string symbol,
            string orderType,
            decimal quantity,
            char side,
            decimal price = 0m
            )
        {
            if (_sessionID == null)
            {
                Console.WriteLine("Cannot send message: No active session.");
                return;
            }
            QuickFix.Message order;

            if (orderType == "MKT")
            {
                // Construct the message
                order = new QuickFix.Message().BuildMarketOrder(symbol, quantity, side);
            }
            else if(orderType == "LMT")
            {
                // Construct the message
                order = new QuickFix.Message().BuildLimitOrder(symbol, quantity, side, price);
            }
            else
            {
                throw new Exception("Invalid order type.");
            }


            // Send the message
            try
            {
                if (Session.SendToTarget(order, _sessionID))
                {
                    Console.WriteLine($"Message sent successfully");
                }
                else
                {
                    Console.WriteLine("Message could not be sent.");
                    throw new Exception("Application had issues sending message");
                }
            }
            catch (Exception ex)
            {
                Console.WriteLine($"Could not send message: {ex.Message}");
                throw;
            }
        }
    }
}

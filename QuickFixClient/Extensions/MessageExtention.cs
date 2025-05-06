using QuickFix.Fields;

namespace QuickFixClient.Extensions
{
    public static class MessageExtentions
    {
        public static string ReadableString(this QuickFix.Message fixMessage)
        {
            string rawFixMessage = fixMessage.ToString();
            // Use regex to insert '|' before each key-value pair except at the start of the string
            string formattedMessage = System.Text.RegularExpressions.Regex.Replace(rawFixMessage, "(?<!^)(\\d+=)", "|$1") + "|";
            return formattedMessage;
        }

        public static QuickFix.Message buildLogon(this QuickFix.Message fixMessage)
        {
            fixMessage.SetField(new StringField(1137, "FIX50SP2"));
            fixMessage.Header.HEADER_FIELD_ORDER = [8, 9, 35, 34, 49, 56, 52, 98, 108];
            fixMessage.Trailer.TRAILER_FIELD_ORDER = [1137, 10];

            return fixMessage;
        }

        public static QuickFix.Message buildHeartBeat(this QuickFix.Message fixMessage)
        {
            fixMessage.Header.SetField(new MsgType("0"));
            fixMessage.Header.HEADER_FIELD_ORDER = [8, 9, 35, 34, 49, 52, 56];
            fixMessage.Trailer.TRAILER_FIELD_ORDER = [10];
            return fixMessage;
        }

        public static QuickFix.Message BuildMarketOrder(
            this QuickFix.Message fixMessage, 
            string symbol,
            decimal quantity,
            char side,
            decimal price = 0m
            )
        {
            // Header Fields (FIX Protocol Standard)
            fixMessage.Header.SetField(new MsgType(MsgType.ORDER_SINGLE));

            // Body Fields (New Order Fields)
            fixMessage.SetField(new ClOrdID(Guid.NewGuid().ToString()));
            fixMessage.SetField(new Symbol(symbol));
            fixMessage.SetField(new Side(side));
            fixMessage.SetField(new OrdType(OrdType.MARKET));
            fixMessage.SetField(new OrderQty(quantity));
            fixMessage.SetField(new TimeInForce(TimeInForce.DAY));
            fixMessage.SetField(new TransactTime(DateTime.UtcNow));
            fixMessage.SetField(new HandlInst(HandlInst.AUTOMATED_EXECUTION_ORDER_PRIVATE));

            // Set the order of fields
            fixMessage.Header.HEADER_FIELD_ORDER = [8, 9, 35, 34, 49, 52, 56];

            return fixMessage;
        }

        public static QuickFix.Message BuildLimitOrder(
            this QuickFix.Message fixMessage,
            string symbol,
            decimal quantity,
            char side,
            decimal price
            )
        {
            // Header Fields (FIX Protocol Standard)
            fixMessage.Header.SetField(new MsgType(MsgType.ORDER_SINGLE));

            // Body Fields (New Order Fields)
            fixMessage.SetField(new ClOrdID(Guid.NewGuid().ToString()));
            fixMessage.SetField(new Symbol(symbol));
            fixMessage.SetField(new Side(side));
            fixMessage.SetField(new OrdType(OrdType.LIMIT));
            fixMessage.SetField(new OrderQty(quantity));
            fixMessage.SetField(new Price(price));
            fixMessage.SetField(new TimeInForce(TimeInForce.DAY));
            fixMessage.SetField(new TransactTime(DateTime.UtcNow));
            fixMessage.SetField(new HandlInst(HandlInst.AUTOMATED_EXECUTION_ORDER_PRIVATE));
            
            // Set the order of fields
            fixMessage.Header.HEADER_FIELD_ORDER = [8, 9, 35, 34, 49, 52, 56];
            
            return fixMessage;
        }

    }
}

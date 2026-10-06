module MySQLTypes where

import Database.MySQL.Base (MySQLValue(..))
import qualified Data.Text as T
import Data.Time (Day, TimeOfDay)
import Data.Int (Int32)

-- Int -> MySQLValue
toMySQLInt :: Int -> MySQLValue
toMySQLInt n = MySQLInt32 (fromIntegral n)

-- MySQLValue -> Int
fromMySQLInt :: MySQLValue -> Int
fromMySQLInt (MySQLInt8   n) = fromIntegral n
fromMySQLInt (MySQLInt8U  n) = fromIntegral n
fromMySQLInt (MySQLInt16  n) = fromIntegral n
fromMySQLInt (MySQLInt16U n) = fromIntegral n
fromMySQLInt (MySQLInt32  n) = fromIntegral n
fromMySQLInt (MySQLInt32U n) = fromIntegral n
fromMySQLInt (MySQLInt64  n) = fromIntegral n
fromMySQLInt (MySQLInt64U n) = fromIntegral n
fromMySQLInt v = error ("The INT value was expected, but received: " ++ show v)

-- String <-> MySQLValue (Text)
toMySQLString :: String -> MySQLValue
toMySQLString s = MySQLText (T.pack s)

fromMySQLString :: MySQLValue -> String
fromMySQLString (MySQLText t) = T.unpack t
fromMySQLString v = error ("The STRING value was expected, but received: " ++ show v)

-- Day <-> MySQLValue
toMySQLDay :: Day -> MySQLValue
toMySQLDay = MySQLDate

fromMySQLDay :: MySQLValue -> Day
fromMySQLDay (MySQLDate d) = d
fromMySQLDay v = error ("The DATE value was expected, but received: " ++ show v)

-- TimeOfDay <-> MySQLValue
toMySQLTimeOfDay :: TimeOfDay -> MySQLValue
toMySQLTimeOfDay t = MySQLTime 0 t   -- 0 = не від'ємний час

fromMySQLTimeOfDay :: MySQLValue -> TimeOfDay
fromMySQLTimeOfDay (MySQLTime _ t) = t
fromMySQLTimeOfDay v = error ("The TIME value was expected, but received: " ++ show v)
{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE ScopedTypeVariables #-}

module DB where

import Database.MySQL.Base
import qualified System.IO.Streams as Streams
import System.Environment (lookupEnv)
import Data.String (fromString)
import Data.List (intercalate)
import Data.Proxy (Proxy(..))

import Entity
import Types
import MySQLTypes

connectDB :: IO MySQLConn
connectDB = do
  maybePassword <- lookupEnv "DB_PASSWORD"
  password <- case maybePassword of
    Just p  -> return p
    Nothing -> error "Enter DB_PASSWORD in .env.ps1 file"
  connect defaultConnectInfoMB4
    { ciHost     = "127.0.0.1"
    , ciPort     = 3306
    , ciDatabase = "faculty_sport"
    , ciUser     = "haskell_app"
    , ciPassword = fromString password
    }

insertEntity :: forall a. Entity a => MySQLConn -> a -> IO OK
insertEntity conn item = do
  let values = toRow item
      placeholders = intercalate ", " (replicate (length values) "?")
      sql = "INSERT INTO " ++ tableName (Proxy :: Proxy a)
            ++ " VALUES (DEFAULT, " ++ placeholders ++ ")"
  execute conn (fromString sql) values

getAll :: forall a. Entity a => MySQLConn -> IO [a]
getAll conn = do
  let table = tableName (Proxy :: Proxy a)
  (_, inputStream) <- query_ conn (fromString ("SELECT * FROM " ++ table))
  rows <- Streams.toList inputStream
  return (map fromRow rows)

deleteEntity :: forall a. Entity a => MySQLConn -> a -> IO OK
deleteEntity conn item = do
  let sql = "DELETE FROM " ++ tableName (Proxy :: Proxy a) ++ " WHERE id = ?"
  execute conn (fromString sql) [toMySQLInt (entityId item)]

updateEntity :: forall a. Entity a => MySQLConn -> a -> IO OK
updateEntity conn item = do
  let cols = columnNames (Proxy :: Proxy a)
      setClause = intercalate ", " (map (++ " = ?") cols)
      sql = "UPDATE " ++ tableName (Proxy :: Proxy a) 
            ++ " SET " ++ setClause ++ " WHERE id = ?"
  execute conn (fromString sql) (toRow item ++ [toMySQLInt (entityId item)])

getById :: forall a. Entity a => MySQLConn -> Int -> IO (Maybe a)
getById conn i = do
  let sql = "SELECT * FROM " ++ tableName (Proxy :: Proxy a) ++ " WHERE id = ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLInt i]
  rows <- Streams.toList inputStream
  case rows of
    []      -> return Nothing
    (r : _) -> return (Just (fromRow r))
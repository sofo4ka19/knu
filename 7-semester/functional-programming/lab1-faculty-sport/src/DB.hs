{-# LANGUAGE OverloadedStrings #-}
{-# LANGUAGE ScopedTypeVariables #-}

module DB where

import Database.MySQL.Base
import Configuration.Dotenv (loadFile, defaultConfig)
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
  loadFile defaultConfig
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

deleteById :: forall a. Entity a => Proxy a -> MySQLConn -> Int -> IO OK
deleteById _ conn i = do
  let sql = "DELETE FROM " ++ tableName (Proxy :: Proxy a) ++ " WHERE id = ?"
  execute conn (fromString sql) [toMySQLInt i]

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

getStudentsInSection :: MySQLConn -> Int -> IO [Student]
getStudentsInSection conn sectionId = do
  let sql = "SELECT s.id, s.full_name, s.group_name, s.phone \
            \FROM students s \
            \JOIN section_members sm ON s.id = sm.stud_id \
            \WHERE sm.sec_id = ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLInt sectionId]
  rows <- Streams.toList inputStream
  return (map fromRow rows)

getScheduleForSection :: MySQLConn -> Int -> IO [Schedule]
getScheduleForSection conn sectionId = do
  let sql = "SELECT * FROM schedule WHERE sec_id = ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLInt sectionId]
  rows <- Streams.toList inputStream
  return (map fromRow rows)

getSectionsByCoach :: MySQLConn -> Int -> IO [Section]
getSectionsByCoach conn cId = do
  let sql = "SELECT * FROM sections WHERE coach_id = ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLInt cId]
  rows <- Streams.toList inputStream
  return (map fromRow rows)

getCompetitionResults :: MySQLConn -> Int -> IO [CompetitionMember]
getCompetitionResults conn cmpId = do
  let sql = "SELECT * FROM competition_members WHERE comp_id = ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLInt cmpId]
  rows <- Streams.toList inputStream
  return (map fromRow rows)

searchByName :: forall a. Searchable a => MySQLConn -> String -> IO [a]
searchByName conn namePart = do
  let col   = nameColumn (Proxy :: Proxy a)
      table = tableName (Proxy :: Proxy a)
      sql   = "SELECT * FROM " ++ table ++ " WHERE " ++ col ++ " LIKE ?"
  (_, inputStream) <- query conn (fromString sql) [toMySQLString ("%" ++ namePart ++ "%")]
  rows <- Streams.toList inputStream
  return (map fromRow rows)

removeStudentFromSection :: MySQLConn -> Int -> Int -> IO OK
removeStudentFromSection conn sid secid = 
  execute conn "DELETE FROM section_members WHERE stud_id = ? AND sec_id = ?" 
    [toMySQLInt sid, toMySQLInt secid]
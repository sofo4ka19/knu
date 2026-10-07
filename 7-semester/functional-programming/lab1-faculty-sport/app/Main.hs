module Main where

import DB
import Entity
import Types

main :: IO ()
main = do
  conn <- connectDB
  putStrLn "Підключено до бази!"

  -- UPDATE: змінимо телефон студента з id=1
  let updatedStudent = Student { studId = 1, studName = "Марія Іванова", studGroup = "КН-21", studPhone = "+380679999999" }
  _ <- updateEntity conn updatedStudent
  putStrLn "Студента оновлено!"

  -- Перевіримо, що оновилось
  students <- getAll conn :: IO [Student]
  mapM_ (\s -> putStrLn (studName s ++ " (" ++ studGroup s ++ ") " ++ studPhone s)) students

  -- DELETE: видалимо цього ж студента
  _ <- deleteEntity conn updatedStudent
  putStrLn "Студента видалено!"

  -- Перевіримо, що список тепер порожній
  studentsAfterDelete <- getAll conn :: IO [Student]
  print studentsAfterDelete
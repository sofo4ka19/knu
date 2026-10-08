module UI where

import Control.Exception (try, SomeException)
import Text.Read (readMaybe)
import Database.MySQL.Base (MySQLConn, OK)
import Data.Proxy (Proxy(..))
import Data.Char (isDigit)

import DB
import Types

-- ==================== INPUT HELPERS ====================

getIntInput :: String -> IO Int
getIntInput prompt = do
  putStr prompt
  input <- getLine
  case readMaybe input of
    Just n  -> return n
    Nothing -> putStrLn "Please enter a valid integer." >> getIntInput prompt

getStringInput :: String -> IO String
getStringInput prompt = putStr prompt >> getLine

isValidPhone :: String -> Bool
isValidPhone p =
  length p >= 10 &&
  length p <= 13 &&
  case p of
    ('+':rest) -> all isDigit rest
    _          -> all isDigit p

getPhoneInput :: String -> IO String
getPhoneInput prompt = do
  phone <- getStringInput prompt
  if isValidPhone phone
    then return phone
    else do
      putStrLn "Invalid phone format. Example: +380501234567"
      getPhoneInput prompt

-- Search by (partial) name, show matches, Enter = first match, number = explicit id
selectEntityId :: (MySQLConn -> String -> IO [a]) -> (a -> Int) -> (a -> String)
               -> MySQLConn -> String -> IO (Maybe Int)
selectEntityId searchFn getId getLabel conn searchPrompt = do
  namePart <- getStringInput searchPrompt
  matches <- searchFn conn namePart
  case matches of
    [] -> putStrLn "No matches found." >> return Nothing
    _  -> do
      mapM_ (\item -> putStrLn (show (getId item) ++ ". " ++ getLabel item)) matches
      input <- getStringInput "Press Enter for the first match, or type an id: "
      case input of
        "" -> return (Just (getId (head matches)))
        s  -> case readMaybe s of
                Just n  -> return (Just n)
                Nothing -> putStrLn "Invalid input, cancelled." >> return Nothing

runSafely :: IO OK -> IO ()
runSafely action = do
  result <- try action :: IO (Either SomeException OK)
  case result of
    Right _  -> putStrLn "Successfully executed!"
    Left err -> putStrLn ("Database error: " ++ show err)

-- ==================== MAIN MENU ====================

runMenu :: MySQLConn -> IO ()
runMenu conn = do
  putStrLn ""
  putStrLn "=== Sports at the Faculty ==="
  putStrLn "1. Students"
  putStrLn "2. Coaches"
  putStrLn "3. Sections"
  putStrLn "4. Competitions"
  putStrLn "0. Exit"
  choice <- getStringInput "Choose a section: "
  case choice of
    "1" -> studentMenu conn      >> runMenu conn
    "2" -> coachMenu conn        >> runMenu conn
    "3" -> sectionMenu conn      >> runMenu conn
    "4" -> competitionMenu conn  >> runMenu conn
    "0" -> putStrLn "Goodbye!"
    _   -> putStrLn "Invalid choice." >> runMenu conn

-- ==================== STUDENTS ====================

studentMenu :: MySQLConn -> IO ()
studentMenu conn = do
  putStrLn ""
  putStrLn "--- Students ---"
  putStrLn "1. View all"
  putStrLn "2. Add"
  putStrLn "3. Update"
  putStrLn "4. Delete"
  putStrLn "5. Register for a section"
  putStrLn "6. Register for a competition"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowStudents conn               >> studentMenu conn
    "2" -> handleAddStudent conn                 >> studentMenu conn
    "3" -> handleUpdateStudent conn               >> studentMenu conn
    "4" -> handleDeleteStudent conn               >> studentMenu conn
    "5" -> handleRegisterStudentSection conn      >> studentMenu conn
    "6" -> handleRegisterStudentCompetition conn  >> studentMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> studentMenu conn

handleShowStudents :: MySQLConn -> IO ()
handleShowStudents conn = do
  students <- getAll conn :: IO [Student]
  if null students
    then putStrLn "No students available."
    else mapM_ (\s -> putStrLn (show (studId s) ++ ". " ++ studName s ++ " (" ++ studGroup s ++ "), " ++ studPhone s)) students

handleAddStudent :: MySQLConn -> IO ()
handleAddStudent conn = do
  name  <- getStringInput "Full name: "
  group <- getStringInput "Group: "
  phone <- getPhoneInput "Phone (+380...): "
  runSafely (insertEntity conn (Student 0 name group phone))

handleUpdateStudent :: MySQLConn -> IO ()
handleUpdateStudent conn = do
  maybeId <- selectEntityId searchByName studId studName conn "Student's full name (or part of it): "
  case maybeId of
    Nothing  -> return ()
    Just sid -> do
      name  <- getStringInput "New full name: "
      group <- getStringInput "New group: "
      phone <- getPhoneInput "New phone: "
      runSafely (updateEntity conn (Student sid name group phone))

handleDeleteStudent :: MySQLConn -> IO ()
handleDeleteStudent conn = do
  maybeId <- selectEntityId searchByName studId studName conn "Student's full name (or part of it): "
  case maybeId of
    Nothing  -> return ()
    Just sid -> runSafely (deleteById (Proxy :: Proxy Student) conn sid)

handleRegisterStudentSection :: MySQLConn -> IO ()
handleRegisterStudentSection conn = do
  maybeStudId <- selectEntityId searchByName studId studName conn "Student's name: "
  maybeSecId  <- selectEntityId searchByName secId secName conn "Section name: "
  case (maybeStudId, maybeSecId) of
    (Just sid, Just secid) -> runSafely (insertEntity conn (SectionMember 0 sid secid))
    _ -> putStrLn "Operation cancelled."

handleRegisterStudentCompetition :: MySQLConn -> IO ()
handleRegisterStudentCompetition conn = do
  maybeStudId <- selectEntityId searchByName studId studName conn "Student's name: "
  maybeCompId <- selectEntityId searchByName compId compName conn "Competition name: "
  case (maybeStudId, maybeCompId) of
    (Just sid, Just cid) -> do
      result <- getStringInput "Result: "
      runSafely (insertEntity conn (CompetitionMember 0 sid cid result))
    _ -> putStrLn "Operation cancelled."

-- ==================== COACHES ====================

coachMenu :: MySQLConn -> IO ()
coachMenu conn = do
  putStrLn ""
  putStrLn "--- Coaches ---"
  putStrLn "1. View all"
  putStrLn "2. Add"
  putStrLn "3. Update"
  putStrLn "4. Delete"
  putStrLn "5. View sections by this coach"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowCoaches conn        >> coachMenu conn
    "2" -> handleAddCoach conn           >> coachMenu conn
    "3" -> handleUpdateCoach conn        >> coachMenu conn
    "4" -> handleDeleteCoach conn        >> coachMenu conn
    "5" -> handleSectionsByCoach conn    >> coachMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> coachMenu conn

handleShowCoaches :: MySQLConn -> IO ()
handleShowCoaches conn = do
  coaches <- getAll conn :: IO [Coach]
  if null coaches
    then putStrLn "No coaches available."
    else mapM_ (\c -> putStrLn (show (coachId c) ++ ". " ++ coachName c ++ ", " ++ coachPhone c)) coaches

handleAddCoach :: MySQLConn -> IO ()
handleAddCoach conn = do
  name  <- getStringInput "Coach's full name: "
  phone <- getPhoneInput "Phone: "
  runSafely (insertEntity conn (Coach 0 name phone))

handleUpdateCoach :: MySQLConn -> IO ()
handleUpdateCoach conn = do
  maybeId <- selectEntityId searchByName coachId coachName conn "Coach's name (or part of it): "
  case maybeId of
    Nothing  -> return ()
    Just cid -> do
      name  <- getStringInput "New name: "
      phone <- getPhoneInput "New phone: "
      runSafely (updateEntity conn (Coach cid name phone))

handleDeleteCoach :: MySQLConn -> IO ()
handleDeleteCoach conn = do
  maybeId <- selectEntityId searchByName coachId coachName conn "Coach's name (or part of it): "
  case maybeId of
    Nothing  -> return ()
    Just cid -> runSafely (deleteById (Proxy :: Proxy Coach) conn cid)

handleSectionsByCoach :: MySQLConn -> IO ()
handleSectionsByCoach conn = do
  maybeId <- selectEntityId searchByName coachId coachName conn "Coach's name: "
  case maybeId of
    Nothing  -> return ()
    Just cid -> do
      sections <- getSectionsByCoach conn cid
      if null sections
        then putStrLn "This coach has no sections."
        else mapM_ (\s -> putStrLn (show (secId s) ++ ". " ++ secName s)) sections

-- ==================== SECTIONS ====================

sectionMenu :: MySQLConn -> IO ()
sectionMenu conn = do
  putStrLn ""
  putStrLn "--- Sections ---"
  putStrLn "1. View all"
  putStrLn "2. Add"
  putStrLn "3. Update"
  putStrLn "4. Delete"
  putStrLn "5. Students in a section"
  putStrLn "6. Remove a student from a section"
  putStrLn "7. Schedule"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowSections conn            >> sectionMenu conn
    "2" -> handleAddSection conn              >> sectionMenu conn
    "3" -> handleUpdateSection conn           >> sectionMenu conn
    "4" -> handleDeleteSection conn           >> sectionMenu conn
    "5" -> handleStudentsInSection conn       >> sectionMenu conn
    "6" -> handleRemoveStudentFromSection conn >> sectionMenu conn
    "7" -> scheduleMenu conn                  >> sectionMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> sectionMenu conn

handleShowSections :: MySQLConn -> IO ()
handleShowSections conn = do
  sections <- getAll conn :: IO [Section]
  if null sections
    then putStrLn "No sections available."
    else mapM_ (\s -> putStrLn (show (secId s) ++ ". " ++ secName s ++ " (coach id=" ++ show (secCoachId s) ++ ")")) sections

handleAddSection :: MySQLConn -> IO ()
handleAddSection conn = do
  name <- getStringInput "Section name: "
  maybeCoachId <- selectEntityId searchByName coachId coachName conn "Coach's name: "
  case maybeCoachId of
    Just cid -> runSafely (insertEntity conn (Section 0 name cid))
    Nothing  -> putStrLn "Operation cancelled."

handleUpdateSection :: MySQLConn -> IO ()
handleUpdateSection conn = do
  maybeId <- selectEntityId searchByName secId secName conn "Section name (or part of it): "
  case maybeId of
    Nothing -> return ()
    Just secid -> do
      name <- getStringInput "New name: "
      maybeCoachId <- selectEntityId searchByName coachId coachName conn "New coach's name: "
      case maybeCoachId of
        Just cid -> runSafely (updateEntity conn (Section secid name cid))
        Nothing  -> putStrLn "Operation cancelled."

handleDeleteSection :: MySQLConn -> IO ()
handleDeleteSection conn = do
  maybeId <- selectEntityId searchByName secId secName conn "Section name (or part of it): "
  case maybeId of
    Nothing    -> return ()
    Just secid -> runSafely (deleteById (Proxy :: Proxy Section) conn secid)

handleStudentsInSection :: MySQLConn -> IO ()
handleStudentsInSection conn = do
  maybeId <- selectEntityId searchByName secId secName conn "Section name: "
  case maybeId of
    Nothing    -> return ()
    Just secid -> do
      students <- getStudentsInSection conn secid
      if null students
        then putStrLn "No students in this section."
        else mapM_ (\s -> putStrLn (studName s ++ " (" ++ studGroup s ++ ")")) students

handleRemoveStudentFromSection :: MySQLConn -> IO ()
handleRemoveStudentFromSection conn = do
  maybeStudId <- selectEntityId searchByName studId studName conn "Student's name: "
  maybeSecId  <- selectEntityId searchByName secId secName conn "Section name: "
  case (maybeStudId, maybeSecId) of
    (Just sid, Just secid) -> runSafely (removeStudentFromSection conn sid secid)
    _ -> putStrLn "Operation cancelled."

-- Schedule (nested submenu)

scheduleMenu :: MySQLConn -> IO ()
scheduleMenu conn = do
  putStrLn ""
  putStrLn "--- Schedule ---"
  putStrLn "1. View a section's schedule"
  putStrLn "2. Add a class"
  putStrLn "3. Update a class"
  putStrLn "4. Delete a class"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowSchedule conn   >> scheduleMenu conn
    "2" -> handleAddSchedule conn    >> scheduleMenu conn
    "3" -> handleUpdateSchedule conn >> scheduleMenu conn
    "4" -> handleDeleteSchedule conn >> scheduleMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> scheduleMenu conn

handleShowSchedule :: MySQLConn -> IO ()
handleShowSchedule conn = do
  maybeId <- selectEntityId searchByName secId secName conn "Section name: "
  case maybeId of
    Nothing -> return ()
    Just secid -> do
      items <- getScheduleForSection conn secid
      if null items
        then putStrLn "Schedule is empty."
        else mapM_ (\sc -> putStrLn (show (schedId sc) ++ ". " ++ show (schedDay sc) ++ " "
                    ++ show (schedStart sc) ++ "-" ++ show (schedEnd sc) ++ ", " ++ schedPlace sc)) items

handleAddSchedule :: MySQLConn -> IO ()
handleAddSchedule conn = do
  maybeId <- selectEntityId searchByName secId secName conn "Section name: "
  case maybeId of
    Nothing -> return ()
    Just secid -> do
      dayStr   <- getStringInput "Day of week (Monday..Sunday): "
      startStr <- getStringInput "Start time (HH:MM:SS): "
      endStr   <- getStringInput "End time (HH:MM:SS): "
      place    <- getStringInput "Place: "
      case (readMaybe dayStr, readMaybe startStr, readMaybe endStr) of
        (Just day, Just start, Just end) ->
          runSafely (insertEntity conn (Schedule 0 secid day start end place))
        _ -> putStrLn "Invalid day/time format."

handleUpdateSchedule :: MySQLConn -> IO ()
handleUpdateSchedule conn = do
  sid      <- getIntInput "Schedule entry id (check via view): "
  dayStr   <- getStringInput "New day of week: "
  startStr <- getStringInput "New start time (HH:MM:SS): "
  endStr   <- getStringInput "New end time (HH:MM:SS): "
  place    <- getStringInput "New place: "
  secid    <- getIntInput "Section id: "
  case (readMaybe dayStr, readMaybe startStr, readMaybe endStr) of
    (Just day, Just start, Just end) ->
      runSafely (updateEntity conn (Schedule sid secid day start end place))
    _ -> putStrLn "Invalid format."

handleDeleteSchedule :: MySQLConn -> IO ()
handleDeleteSchedule conn = do
  sid <- getIntInput "Schedule entry id to delete: "
  runSafely (deleteById (Proxy :: Proxy Schedule) conn sid)

-- ==================== COMPETITIONS ====================

competitionMenu :: MySQLConn -> IO ()
competitionMenu conn = do
  putStrLn ""
  putStrLn "--- Competitions ---"
  putStrLn "1. View all"
  putStrLn "2. Add"
  putStrLn "3. Update"
  putStrLn "4. Delete"
  putStrLn "5. Participants' results"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowCompetitions conn   >> competitionMenu conn
    "2" -> handleAddCompetition conn     >> competitionMenu conn
    "3" -> handleUpdateCompetition conn  >> competitionMenu conn
    "4" -> handleDeleteCompetition conn  >> competitionMenu conn
    "5" -> handleCompetitionResults conn >> competitionMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> competitionMenu conn

handleShowCompetitions :: MySQLConn -> IO ()
handleShowCompetitions conn = do
  comps <- getAll conn :: IO [Competition]
  if null comps
    then putStrLn "No competitions available."
    else mapM_ (\c -> putStrLn (show (compId c) ++ ". " ++ compName c ++ " (" ++ show (compDate c) ++ ", " ++ compPlace c ++ ")")) comps

handleAddCompetition :: MySQLConn -> IO ()
handleAddCompetition conn = do
  name    <- getStringInput "Competition name: "
  dateStr <- getStringInput "Date (YYYY-MM-DD): "
  place   <- getStringInput "Place: "
  maybeSecId <- selectEntityId searchByName secId secName conn "Section name: "
  case (readMaybe dateStr, maybeSecId) of
    (Just date, Just secid) -> runSafely (insertEntity conn (Competition 0 name date place secid))
    _ -> putStrLn "Invalid data."

handleUpdateCompetition :: MySQLConn -> IO ()
handleUpdateCompetition conn = do
  maybeId <- selectEntityId searchByName compId compName conn "Competition name (or part of it): "
  case maybeId of
    Nothing -> return ()
    Just cid -> do
      name    <- getStringInput "New name: "
      dateStr <- getStringInput "New date (YYYY-MM-DD): "
      place   <- getStringInput "New place: "
      maybeSecId <- selectEntityId searchByName secId secName conn "Section name: "
      case (readMaybe dateStr, maybeSecId) of
        (Just date, Just secid) -> runSafely (updateEntity conn (Competition cid name date place secid))
        _ -> putStrLn "Invalid data."

handleDeleteCompetition :: MySQLConn -> IO ()
handleDeleteCompetition conn = do
  maybeId <- selectEntityId searchByName compId compName conn "Competition name (or part of it): "
  case maybeId of
    Nothing  -> return ()
    Just cid -> runSafely (deleteById (Proxy :: Proxy Competition) conn cid)

handleCompetitionResults :: MySQLConn -> IO ()
handleCompetitionResults conn = do
  maybeId <- selectEntityId searchByName compId compName conn "Competition name: "
  case maybeId of
    Nothing  -> return ()
    Just cid -> do
      results <- getCompetitionResults conn cid
      if null results
        then putStrLn "No participants."
        else mapM_ (\r -> putStrLn ("studId=" ++ show (compMemStudId r) ++ ": " ++ compMemResult r)) results
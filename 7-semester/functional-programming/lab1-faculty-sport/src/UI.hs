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

getStringInputOptional :: String -> String -> IO String
getStringInputOptional prompt oldValue = do
  input <- getStringInput (prompt ++ " [" ++ oldValue ++ "]: ")
  if null input then return oldValue else return input

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
    else putStrLn "Invalid phone format. Example: +380501234567" >> getPhoneInput prompt

getPhoneInputOptional :: String -> String -> IO String
getPhoneInputOptional prompt oldValue = do
  input <- getStringInput (prompt ++ " [" ++ oldValue ++ "]: ")
  if null input
    then return oldValue
    else if isValidPhone input
         then return input
         else putStrLn "Invalid phone format." >> getPhoneInputOptional prompt oldValue

-- Search by (partial) name; show matches; Enter = first match;
-- number = must belong to the shown list, otherwise the operation fails
selectEntity :: (MySQLConn -> String -> IO [a]) -> (a -> Int) -> (a -> String)
             -> MySQLConn -> String -> IO (Maybe a)
selectEntity searchFn getId getLabel conn prompt = do
  namePart <- getStringInput prompt
  matches <- searchFn conn namePart
  case matches of
    [] -> putStrLn "No matches found." >> return Nothing
    _  -> do
      mapM_ (\item -> putStrLn (show (getId item) ++ ". " ++ getLabel item)) matches
      input <- getStringInput "Press Enter for the first match, or type an id: "
      case input of
        "" -> return (Just (head matches))
        s  -> case readMaybe s of
          Just n -> case filter (\item -> getId item == n) matches of
            (x : _) -> return (Just x)
            []      -> putStrLn "That id is not in the list. Operation failed." >> return Nothing
          Nothing -> putStrLn "Invalid input, cancelled." >> return Nothing

-- Same as selectEntity, but Enter with no search text keeps the current id untouched
selectEntityOptional :: (MySQLConn -> String -> IO [a]) -> (a -> Int) -> (a -> String)
                      -> MySQLConn -> String -> Int -> IO (Maybe Int)
selectEntityOptional searchFn getId getLabel conn prompt currentId = do
  namePart <- getStringInput (prompt ++ " [Enter to keep current]: ")
  if null namePart
    then return (Just currentId)
    else fmap (fmap getId) (selectEntity searchFn getId getLabel conn' namePart)
  where
    conn' = conn   -- just to keep signature readable; searchFn is applied below instead
-- Note: to avoid double-prompting, this calls the search directly rather than selectEntity's own prompt.

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
    "1" -> handleShowStudents conn              >> studentMenu conn
    "2" -> handleAddStudent conn                >> studentMenu conn
    "3" -> handleUpdateStudent conn             >> studentMenu conn
    "4" -> handleDeleteStudent conn             >> studentMenu conn
    "5" -> handleRegisterStudentSection conn    >> studentMenu conn
    "6" -> handleRegisterStudentCompetition conn >> studentMenu conn
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
  maybeOld <- selectEntity searchByName studId studName conn "Student's full name (or part of it): "
  case maybeOld of
    Nothing  -> return ()
    Just old -> do
      name  <- getStringInputOptional "New full name" (studName old)
      group <- getStringInputOptional "New group" (studGroup old)
      phone <- getPhoneInputOptional "New phone" (studPhone old)
      runSafely (updateEntity conn (Student (studId old) name group phone))

handleDeleteStudent :: MySQLConn -> IO ()
handleDeleteStudent conn = do
  maybeStudent <- selectEntity searchByName studId studName conn "Student's full name (or part of it): "
  case maybeStudent of
    Nothing      -> return ()
    Just student -> runSafely (deleteById (Proxy :: Proxy Student) conn (studId student))

handleRegisterStudentSection :: MySQLConn -> IO ()
handleRegisterStudentSection conn = do
  maybeStudent <- selectEntity searchByName studId studName conn "Student's name: "
  case maybeStudent of
    Nothing -> putStrLn "Student not found. Operation cancelled."
    Just student -> do
      maybeSection <- selectEntity searchByName secId secName conn "Section name: "
      case maybeSection of
        Nothing      -> putStrLn "Section not found. Operation cancelled."
        Just section -> do
          already <- isStudentInSection conn (studId student) (secId section)
          if already
            then putStrLn "This student is already registered in this section."
            else runSafely (insertEntity conn (SectionMember 0 (studId student) (secId section)))

handleRegisterStudentCompetition :: MySQLConn -> IO ()
handleRegisterStudentCompetition conn = do
  maybeStudent <- selectEntity searchByName studId studName conn "Student's name: "
  case maybeStudent of
    Nothing -> putStrLn "Student not found. Operation cancelled."
    Just student -> do
      maybeComp <- selectEntity searchByName compId compName conn "Competition name: "
      case maybeComp of
        Nothing   -> putStrLn "Competition not found. Operation cancelled."
        Just comp -> do
          already <- isStudentInCompetition conn (studId student) (compId comp)
          if already
            then putStrLn "This student is already registered in this competition."
            else do
              result <- getStringInput "Result: "
              runSafely (insertEntity conn (CompetitionMember 0 (studId student) (compId comp) result))

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
    "1" -> handleShowCoaches conn     >> coachMenu conn
    "2" -> handleAddCoach conn        >> coachMenu conn
    "3" -> handleUpdateCoach conn     >> coachMenu conn
    "4" -> handleDeleteCoach conn     >> coachMenu conn
    "5" -> handleSectionsByCoach conn >> coachMenu conn
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
  maybeOld <- selectEntity searchByName coachId coachName conn "Coach's name (or part of it): "
  case maybeOld of
    Nothing  -> return ()
    Just old -> do
      name  <- getStringInputOptional "New name" (coachName old)
      phone <- getPhoneInputOptional "New phone" (coachPhone old)
      runSafely (updateEntity conn (Coach (coachId old) name phone))

handleDeleteCoach :: MySQLConn -> IO ()
handleDeleteCoach conn = do
  maybeCoach <- selectEntity searchByName coachId coachName conn "Coach's name (or part of it): "
  case maybeCoach of
    Nothing    -> return ()
    Just coach -> runSafely (deleteById (Proxy :: Proxy Coach) conn (coachId coach))

handleSectionsByCoach :: MySQLConn -> IO ()
handleSectionsByCoach conn = do
  maybeCoach <- selectEntity searchByName coachId coachName conn "Coach's name: "
  case maybeCoach of
    Nothing    -> return ()
    Just coach -> do
      sections <- getSectionsByCoach conn (coachId coach)
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
    "1" -> handleShowSections conn             >> sectionMenu conn
    "2" -> handleAddSection conn               >> sectionMenu conn
    "3" -> handleUpdateSection conn            >> sectionMenu conn
    "4" -> handleDeleteSection conn            >> sectionMenu conn
    "5" -> handleStudentsInSection conn        >> sectionMenu conn
    "6" -> handleRemoveStudentFromSection conn >> sectionMenu conn
    "7" -> scheduleMenu conn                   >> sectionMenu conn
    "0" -> return ()
    _   -> putStrLn "Invalid choice." >> sectionMenu conn

handleShowSections :: MySQLConn -> IO ()
handleShowSections conn = do
  sections <- getSectionsWithCoachNames conn
  if null sections
    then putStrLn "No sections available."
    else mapM_ (\(i, n, cn) -> putStrLn (show i ++ ". " ++ n ++ " (coach: " ++ cn ++ ")")) sections

handleAddSection :: MySQLConn -> IO ()
handleAddSection conn = do
  name <- getStringInput "Section name: "
  maybeCoach <- selectEntity searchByName coachId coachName conn "Coach's name: "
  case maybeCoach of
    Nothing    -> putStrLn "Coach not found. Operation cancelled."
    Just coach -> runSafely (insertEntity conn (Section 0 name (coachId coach)))

handleUpdateSection :: MySQLConn -> IO ()
handleUpdateSection conn = do
  maybeOld <- selectEntity searchByName secId secName conn "Section name (or part of it): "
  case maybeOld of
    Nothing  -> return ()
    Just old -> do
      name <- getStringInputOptional "New name" (secName old)
      input <- getStringInput "New coach's name (or part of it) [Enter to keep current]: "
      if null input
        then runSafely (updateEntity conn (Section (secId old) name (secCoachId old)))
        else do
          matches <- searchByName conn input :: IO [Coach]
          case matches of
            [] -> putStrLn "No matching coach found. Operation cancelled."
            _  -> do
              mapM_ (\c -> putStrLn (show (coachId c) ++ ". " ++ coachName c)) matches
              pick <- getStringInput "Press Enter for the first match, or type an id: "
              let chosen = case pick of
                    ""  -> Just (head matches)
                    s   -> case readMaybe s of
                             Just n  -> case filter ((== n) . coachId) matches of
                                          (x:_) -> Just x
                                          []    -> Nothing
                             Nothing -> Nothing
              case chosen of
                Just coach -> runSafely (updateEntity conn (Section (secId old) name (coachId coach)))
                Nothing    -> putStrLn "That id is not in the list. Operation failed."

handleDeleteSection :: MySQLConn -> IO ()
handleDeleteSection conn = do
  maybeSection <- selectEntity searchByName secId secName conn "Section name (or part of it): "
  case maybeSection of
    Nothing  -> return ()
    Just sec -> runSafely (deleteById (Proxy :: Proxy Section) conn (secId sec))

handleStudentsInSection :: MySQLConn -> IO ()
handleStudentsInSection conn = do
  maybeSection <- selectEntity searchByName secId secName conn "Section name: "
  case maybeSection of
    Nothing  -> return ()
    Just sec -> do
      students <- getStudentsInSection conn (secId sec)
      if null students
        then putStrLn "No students in this section."
        else mapM_ (\s -> putStrLn (studName s ++ " (" ++ studGroup s ++ ")")) students

handleRemoveStudentFromSection :: MySQLConn -> IO ()
handleRemoveStudentFromSection conn = do
  maybeStudent <- selectEntity searchByName studId studName conn "Student's name: "
  case maybeStudent of
    Nothing -> putStrLn "Student not found."
    Just student -> do
      sections <- getSectionsForStudent conn (studId student)
      if null sections
        then putStrLn "This student is not registered in any section."
        else do
          mapM_ (\s -> putStrLn (show (secId s) ++ ". " ++ secName s)) sections
          secIdInput <- getIntInput "Enter section id to remove from: "
          if secIdInput `elem` map secId sections
            then runSafely (removeStudentFromSection conn (studId student) secIdInput)
            else putStrLn "This id is not in the list. Operation failed."

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
  maybeSection <- selectEntity searchByName secId secName conn "Section name: "
  case maybeSection of
    Nothing  -> return ()
    Just sec -> do
      items <- getScheduleForSection conn (secId sec)
      if null items
        then putStrLn "Schedule is empty."
        else mapM_ (\sc -> putStrLn (show (schedId sc) ++ ". " ++ show (schedDay sc) ++ " "
                    ++ show (schedStart sc) ++ "-" ++ show (schedEnd sc) ++ ", " ++ schedPlace sc)) items

handleAddSchedule :: MySQLConn -> IO ()
handleAddSchedule conn = do
  maybeSection <- selectEntity searchByName secId secName conn "Section name: "
  case maybeSection of
    Nothing  -> return ()
    Just sec -> do
      dayStr   <- getStringInput "Day of week (Monday..Sunday): "
      startStr <- getStringInput "Start time (HH:MM:SS): "
      endStr   <- getStringInput "End time (HH:MM:SS): "
      place    <- getStringInput "Place: "
      case (readMaybe dayStr, readMaybe startStr, readMaybe endStr) of
        (Just day, Just start, Just end) ->
          runSafely (insertEntity conn (Schedule 0 (secId sec) day start end place))
        _ -> putStrLn "Invalid day/time format."

handleUpdateSchedule :: MySQLConn -> IO ()
handleUpdateSchedule conn = do
  sid <- getIntInput "Schedule entry id (check via view): "
  maybeOld <- getScheduleById conn sid
  case maybeOld of
    Nothing  -> putStrLn "No schedule entry with this id."
    Just old -> do
      dayStr   <- getStringInputOptional "New day of week" (show (schedDay old))
      startStr <- getStringInputOptional "New start time (HH:MM:SS)" (show (schedStart old))
      endStr   <- getStringInputOptional "New end time (HH:MM:SS)" (show (schedEnd old))
      place    <- getStringInputOptional "New place" (schedPlace old)
      case (readMaybe dayStr, readMaybe startStr, readMaybe endStr) of
        (Just day, Just start, Just end) ->
          runSafely (updateEntity conn (Schedule sid (schedSecId old) day start end place))
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
  putStrLn "6. Update a result"
  putStrLn "0. Back"
  choice <- getStringInput "Choose an action: "
  case choice of
    "1" -> handleShowCompetitions conn        >> competitionMenu conn
    "2" -> handleAddCompetition conn          >> competitionMenu conn
    "3" -> handleUpdateCompetition conn       >> competitionMenu conn
    "4" -> handleDeleteCompetition conn       >> competitionMenu conn
    "5" -> handleCompetitionResults conn      >> competitionMenu conn
    "6" -> handleUpdateCompetitionResult conn >> competitionMenu conn
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
  maybeSection <- selectEntity searchByName secId secName conn "Section name: "
  case (readMaybe dateStr, maybeSection) of
    (Just date, Just sec) -> runSafely (insertEntity conn (Competition 0 name date place (secId sec)))
    _ -> putStrLn "Invalid data or section not found."

handleUpdateCompetition :: MySQLConn -> IO ()
handleUpdateCompetition conn = do
  maybeOld <- selectEntity searchByName compId compName conn "Competition name (or part of it): "
  case maybeOld of
    Nothing  -> return ()
    Just old -> do
      name    <- getStringInputOptional "New name" (compName old)
      dateStr <- getStringInputOptional "New date (YYYY-MM-DD)" (show (compDate old))
      place   <- getStringInputOptional "New place" (compPlace old)
      input   <- getStringInput "New section name (or part of it) [Enter to keep current]: "
      case readMaybe dateStr of
        Nothing -> putStrLn "Invalid date."
        Just date ->
          if null input
            then runSafely (updateEntity conn (Competition (compId old) name date place (compSecId old)))
            else do
              matches <- searchByName conn input :: IO [Section]
              case matches of
                [] -> putStrLn "No matching section found. Operation cancelled."
                _  -> runSafely (updateEntity conn (Competition (compId old) name date place (secId (head matches))))

handleDeleteCompetition :: MySQLConn -> IO ()
handleDeleteCompetition conn = do
  maybeComp <- selectEntity searchByName compId compName conn "Competition name (or part of it): "
  case maybeComp of
    Nothing   -> return ()
    Just comp -> runSafely (deleteById (Proxy :: Proxy Competition) conn (compId comp))

handleCompetitionResults :: MySQLConn -> IO ()
handleCompetitionResults conn = do
  maybeComp <- selectEntity searchByName compId compName conn "Competition name: "
  case maybeComp of
    Nothing   -> return ()
    Just comp -> do
      results <- getCompetitionResultsWithNames conn (compId comp)
      if null results
        then putStrLn "No participants."
        else mapM_ (\(_, n, r) -> putStrLn (n ++ ": " ++ r)) results

handleUpdateCompetitionResult :: MySQLConn -> IO ()
handleUpdateCompetitionResult conn = do
  maybeComp <- selectEntity searchByName compId compName conn "Competition name: "
  case maybeComp of
    Nothing   -> putStrLn "Competition not found."
    Just comp -> do
      results <- getCompetitionResultsWithNames conn (compId comp)
      if null results
        then putStrLn "No participants."
        else do
          mapM_ (\(i, n, r) -> putStrLn (show i ++ ". " ++ n ++ ": " ++ r)) results
          sid <- getIntInput "Enter student id to update result for: "
          if sid `elem` map (\(i, _, _) -> i) results
            then do
              newResult <- getStringInput "New result: "
              runSafely (updateCompetitionResult conn sid (compId comp) newResult)
            else putStrLn "This id is not in the list. Operation failed."
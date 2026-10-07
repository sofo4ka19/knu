module Entity where

import Types
import Database.MySQL.Base (MySQLValue)
import MySQLTypes
import Data.Time(DayOfWeek)
import Data.Proxy (Proxy(..))

class Entity a where
  tableName    :: Proxy a -> String
  columnNames :: Proxy a -> [String]
  toRow        :: a -> [MySQLValue]
  fromRow      :: [MySQLValue] -> a
  entityId     :: a -> Int

instance Entity Student where
  tableName _ = "students"
  columnNames _ = ["full_name", "group_name", "phone"]

  fromRow [i, name, group, phone] = Student
    { studId    = fromMySQLInt i
    , studName  = fromMySQLString name
    , studGroup = fromMySQLString group
    , studPhone = fromMySQLString phone
    }
  fromRow row = error ("Wrong number of columns for Student: " ++ show row)

  entityId = studId

  toRow s =
    [ toMySQLString (studName s)
    , toMySQLString (studGroup s)
    , toMySQLString (studPhone s)
    ]

instance Entity Coach where
  tableName _ = "coaches"
  columnNames _ = ["full_name", "phone"]

  fromRow [i, name, phone] = Coach
    { coachId    = fromMySQLInt i
    , coachName  = fromMySQLString name
    , coachPhone = fromMySQLString phone
    }
  fromRow row = error ("Wrong number of columns for Coach: " ++ show row)

  entityId = coachId

  toRow c =
    [ toMySQLString (coachName c)
    , toMySQLString (coachPhone c)
    ]

instance Entity Section where
  tableName _ = "sections"
  columnNames _ = ["name", "coach_id"]

  fromRow [i, name, coachid] = Section
    { secId      = fromMySQLInt i
    , secName    = fromMySQLString name
    , secCoachId = fromMySQLInt coachid
    }
  fromRow row = error ("Wrong number of columns for Section: " ++ show row)

  entityId = secId

  toRow s =
    [ toMySQLString (secName s)
    , toMySQLInt (secCoachId s)
    ]

instance Entity SectionMember where
  tableName _ = "section_members"
  columnNames _ = ["stud_id", "sec_id"]

  fromRow [i, studentId, sectionId] = SectionMember
    { secMemId     = fromMySQLInt i
    , secMemStudId = fromMySQLInt studentId
    , secMemSecId  = fromMySQLInt sectionId
    }
  fromRow row = error ("Wrong number of columns for SectionMember: " ++ show row)

  entityId = secMemId

  toRow sm =
    [ toMySQLInt (secMemStudId sm)
    , toMySQLInt (secMemSecId sm)
    ]

instance Entity Schedule where
  tableName _ = "schedule"
  columnNames _ = ["sec_id", "day_of_week", "start_time", "end_time", "place"]

  fromRow [i, sectionId, day, start, end, place] = Schedule
    { schedId    = fromMySQLInt i
    , schedSecId = fromMySQLInt sectionId
    , schedDay   = read (fromMySQLString day) :: DayOfWeek
    , schedStart = fromMySQLTimeOfDay start
    , schedEnd   = fromMySQLTimeOfDay end
    , schedPlace = fromMySQLString place
    }
  fromRow row = error ("Wrong number of columns for Schedule: " ++ show row)

  entityId = schedId

  toRow s =
    [ toMySQLInt (schedSecId s)
    , toMySQLString (show (schedDay s))
    , toMySQLTimeOfDay (schedStart s)
    , toMySQLTimeOfDay (schedEnd s)
    , toMySQLString (schedPlace s)
    ]

instance Entity Competition where
  tableName _ = "competitions"
  columnNames _ = ["name", "date", "place", "sec_id"]

  fromRow [i, name, date, place, sectionId] = Competition
    { compId    = fromMySQLInt i
    , compName  = fromMySQLString name
    , compDate  = fromMySQLDay date
    , compPlace = fromMySQLString place
    , compSecId = fromMySQLInt sectionId
    }
  fromRow row = error ("Wrong number of columns for Competition: " ++ show row)

  entityId = compId

  toRow c =
    [ toMySQLString (compName c)
    , toMySQLDay (compDate c)
    , toMySQLString (compPlace c)
    , toMySQLInt (compSecId c)
    ]

instance Entity CompetitionMember where
  tableName _ = "competition_members"
  columnNames _ = ["stud_id", "comp_id", "result"]
  fromRow [i, studentId, competitionId, result] = CompetitionMember
    { compMemId     = fromMySQLInt i
    , compMemStudId = fromMySQLInt studentId
    , compMemCompId = fromMySQLInt competitionId
    , compMemResult = fromMySQLString result
    }
  fromRow row = error ("Wrong number of columns for CompetitionMember: " ++ show row)
  entityId = compMemId
  toRow cm =
    [ toMySQLInt (compMemStudId cm)
    , toMySQLInt (compMemCompId cm)
    , toMySQLString (compMemResult cm)
    ]
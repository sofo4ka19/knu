module Types where

import Data.Time(DayOfWeek, TimeOfDay, Day)

data Student = Student
  { studId      :: Int
  , studName    :: String
  , studGroup   :: String
  , studPhone   :: String
  } deriving Show

data Coach = Coach
  { coachId     :: Int
  , coachName   :: String
  , coachPhone  :: String
  , coachSpec   :: String
  } deriving Show

data Section = Section
  { secId       :: Int
  , secName     :: String
  , secCoachId  :: Int
  , secDesc     :: String
  } deriving Show

data SectionMember = SectionMember
  { secMemId     :: Int
  , secMemStudId :: Int
  , secMemSecId  :: Int
  } deriving Show

data Schedule = Schedule
  { schedId    :: Int
  , schedSecId :: Int
  , schedDay   :: DayOfWeek
  , schedStart :: TimeOfDay
  , schedEnd   :: TimeOfDay
  , schedPlace :: String
  } deriving Show

data Competition = Competition
  { compId      :: Int
  , compName    :: String
  , compDate    :: Day
  , compPlace   :: String
  , compSecId   :: Int
  } deriving Show

data CompetitionMember = CompetitionMember
  { compMemId     :: Int
  , compMemStudId :: Int
  , compMemCompId :: Int
  , compMemResult :: String
  } deriving Show
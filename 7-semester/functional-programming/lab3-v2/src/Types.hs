module Types
  ( Symbol
  , Word (..)
  , Punctuation (..)
  , Token (..)
  , Sentence (..)
  ) where

import Prelude hiding (Word)

type Symbol = Char

newtype Word = Word [Symbol]
  deriving (Eq, Show)

newtype Punctuation = Punctuation Symbol
  deriving (Eq, Show)

data Token
  = TWord  Word
  | TPunct Punctuation
  deriving (Eq, Show)

newtype Sentence = Sentence [Token]
  deriving (Eq, Show)
module Render (render) where

import Types (Punctuation (..), Sentence (..), Token (..), Word (..))

showToken :: Token -> String
showToken (TWord (Word w))         = w
showToken (TPunct (Punctuation p)) = [p]

noSpaceBefore :: Token -> Bool
noSpaceBefore (TPunct (Punctuation p)) = p `elem` ".,;:!?…)]}»”"
noSpaceBefore _                        = False

noSpaceAfter :: Token -> Bool
noSpaceAfter (TPunct (Punctuation p)) = p `elem` "([{«“"
noSpaceAfter _                        = False

render :: Sentence -> String
render (Sentence ts) = go ts
  where
    go []          = ""
    go [t]         = showToken t
    go (a : b : r) = showToken a ++ sep a b ++ go (b : r)
    sep a b
      | noSpaceAfter a || noSpaceBefore b = ""
      | otherwise                         = " "
module Render (render) where

import Types (Punctuation (..), Sentence (..), Token (..), Word (..))

showToken :: Token -> String
showToken (TWord _ (Word w))         = w
showToken (TPunct _ (Punctuation p)) = [p]

hasSpace :: Token -> Bool
hasSpace (TWord sp _)  = sp
hasSpace (TPunct sp _) = sp

render :: Sentence -> String
render (Sentence [])       = ""
render (Sentence (t : ts)) = showToken t ++ concatMap piece ts
  where
    piece x = (if hasSpace x then " " else "") ++ showToken x
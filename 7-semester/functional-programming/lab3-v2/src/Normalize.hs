module Normalize (normalize) where

-- | Замінює табуляції, переноси рядків та послідовності пробілів
--   одним пробілом; прибирає пробіли на краях.
normalize :: String -> String
normalize = unwords . words
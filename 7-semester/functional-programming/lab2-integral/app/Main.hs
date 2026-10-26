module Main where
import Control.Concurrent (getNumCapabilities)

main :: IO ()
main = getNumCapabilities >>= \n -> putStrLn ("Capabilities: " ++ show n)
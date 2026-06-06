// scala code example

object Counter {

  var count: Int = 0
  var active: Boolean = false
  var label: String = "counter"

  /* start the counter with the initial value and limit */
  def start(initial: Int, limit: Int): Unit = {
    count = initial
    active = true
  }

  def stop(): Unit = {
    active = false
  }

  def check(): Boolean = {
    if (active) {
      return true
    } else {
      return false
    }
  }

  def negated(): Int = -count

  def inverted(): Int = ~count

  def isNotActive(): Boolean = !active
}

object Main {

  def main(args: Array[String]): Unit = {
    val initial: Int = 10
    val limit: Int = 100
    Counter.start(initial, limit)
    val result: Int = Counter.negated()
  }
}
```json
"attr_name": {
  "1": list of attrs,
  "0": list of attrs,
  "in": list of attrs
}
```

In case of many attributes, probability should be structured in such way when structuring values `x1, x2`


| x1  | x2  | P(x3=T if x1,x2) | P(x3=F if x1,x2) |
|-----|-----|------------------|------------------|
| F   | F   | a                | e                |
| F   | T   | b                | f                |
| T   | F   | c                | g                |
| T   | T   | d                | h                |
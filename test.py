from num2words import num2words

# Most common usage.
print(num2words(1))

# Other variants, according to the type of article.
print(num2words(1, to='ordinal', lang='ru'))
print(num2words(1, to='ordinal_num', lang='ru'))
print(num2words(1, to='year', lang='ru'))
print(num2words(1, to='currency', lang='ru'))

# Language Support.
print(type(num2words(36, lang='ru')))
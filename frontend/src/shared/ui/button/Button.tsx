import { ButtonProps, Button as ChakraButton } from '@chakra-ui/react'

export const Button = ({ children, ...props }: ButtonProps) => (
  <ChakraButton
    {...props}
    bg={'blue.100'}
    color={'white'}
    borderRadius={'10px'}
    p={'9px 16px'}
    fontSize={'14px'}
    fontWeight={400}
    cursor={'pointer'}
    _hover={{ bg: 'gray.500' }}
  >
    {children}
  </ChakraButton>
)

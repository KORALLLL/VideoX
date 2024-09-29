import { Button } from '@chakra-ui/react'
import { IMenuButton } from './type'

function MenuButton({ children, onClick, active }: IMenuButton) {
  return (
    <Button
      w={'42px'}
      h={'42px'}
      p="0"
      borderRadius={'100%'}
      onClick={onClick}
      bg="white"
      filter={active ? `drop-shadow(0 0 10px rgba(81, 172, 239, .5))` : ''}
      _hover={{ bg: 'gray.200' }}
      _active={{ bg: 'transparent' }}
      _focus={{ boxShadow: 'none' }}
    >
      {children}
    </Button>
  )
}

export default MenuButton

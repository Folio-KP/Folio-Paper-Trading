import {Navbar, Nav, Container, Form, Button, Row, Col, InputGroup} from 'react-bootstrap';
import {Link} from 'react-router-dom';
import './Navbar.css'

const MainNavbar = () => {
   return (
    <Navbar bg="dark" data-bs-theme="dark" expand="lg">
      <Container fluid className='algin-items-center'>
        <Navbar.Toggle aria-controls="basic-navbar-nav"className='me-3'/>
        <Navbar.Brand as={Link} to="/" className='me-3'>Folio</Navbar.Brand>
        <Form className="d-flex flex-grow-1 me-3">
          <InputGroup className="flex-grow-1 search-form">
            <Form.Control type="text" placeholder="Search for stocks" className="flex-grow-1"/>
            <Button type="submit" variant="outline-success">
              Search
            </Button>
          </InputGroup>
        </Form>
        <Navbar.Collapse id="basic-navbar-nav" className='me-3 flex-grow-0'>
          <Nav className="me-3">
            <Nav.Link as={Link} to="/">Portfolio</Nav.Link>
            <Nav.Link as={Link} to="/leaderboard">Leaderboard</Nav.Link>
            <Nav.Link as={Link} to="/about">About</Nav.Link>
          </Nav>
        </Navbar.Collapse>
        <Button as={Link} to="/login" variant="outline-success" className="me-3">Sign in</Button>
      </Container>
    </Navbar>
  )
}

export default MainNavbar;